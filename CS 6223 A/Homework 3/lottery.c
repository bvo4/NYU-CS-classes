#include "types.h"
#include "defs.h"
#include "param.h"
#include "memlayout.h"
#include "mmu.h"
#include "x86.h"
#include "proc.h"
#include "spinlock.h"

#include "random.h"

#define DEBUG 0

int AllTickets;			//Seed

struct {
  struct spinlock lock;
  struct proc proc[NPROC];
} ptable;

static struct proc *initproc;

int nextpid = 1;
extern void forkret(void);
extern void trapret(void);

static void wakeup1(void *chan);

void setTicketsNice(struct proc *p, int ticket, int NewNice);
void AlterNice(struct proc *p, int NewNice);

void
pinit(void)
{
  initlock(&ptable.lock, "ptable");
}

//PAGEBREAK: 32
// Look in the process table for an UNUSED proc.
// If found, change state to EMBRYO and initialize
// state required to run in the kernel.
// Otherwise return 0.
static struct proc*
allocproc(void)
{
  struct proc *p;
  char *sp;

  acquire(&ptable.lock);
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++)
    if(p->state == UNUSED)
      goto found;
  release(&ptable.lock);
  return 0;

found:
  p->state = EMBRYO;
  p->pid = nextpid++;
  p->tickets = 0;
  p->nice = 0;
  release(&ptable.lock);

  // Allocate kernel stack.
  if((p->kstack = kalloc()) == 0){
    p->state = UNUSED;
    return 0;
  }
  sp = p->kstack + KSTACKSIZE;
  
  // Leave room for trap frame.
  sp -= sizeof *p->tf;
  p->tf = (struct trapframe*)sp;
  
  // Set up new context to start executing at forkret,
  // which returns to trapret.
  sp -= 4;
  *(uint*)sp = (uint)trapret;

  sp -= sizeof *p->context;
  p->context = (struct context*)sp;
  memset(p->context, 0, sizeof *p->context);
  p->context->eip = (uint)forkret;

  return p;
}

//PAGEBREAK: 32
// Set up first user process.
void
userinit(void)
{
  struct proc *p;
  extern char _binary_initcode_start[], _binary_initcode_size[];
  
  p = allocproc();
  initproc = p;
  if((p->pgdir = setupkvm()) == 0)
    panic("userinit: out of memory?");
  inituvm(p->pgdir, _binary_initcode_start, (int)_binary_initcode_size);
  p->sz = PGSIZE;
  memset(p->tf, 0, sizeof(*p->tf));
  p->tf->cs = (SEG_UCODE << 3) | DPL_USER;
  p->tf->ds = (SEG_UDATA << 3) | DPL_USER;
  p->tf->es = p->tf->ds;
  p->tf->ss = p->tf->ds;
  p->tf->eflags = FL_IF;
  p->tf->esp = PGSIZE;
  p->tf->eip = 0;  // beginning of initcode.S

  safestrcpy(p->name, "initcode", sizeof(p->name));
  p->cwd = namei("/");

  p->state = RUNNABLE;
}

// Grow current process's memory by n bytes.
// Return 0 on success, -1 on failure.
int
growproc(int n)
{
  uint sz;
  
  sz = proc->sz;
  if(n > 0){
    if((sz = allocuvm(proc->pgdir, sz, sz + n)) == 0)
      return -1;
  } else if(n < 0){
    if((sz = deallocuvm(proc->pgdir, sz, sz + n)) == 0)
      return -1;
  }
  proc->sz = sz;
  switchuvm(proc);
  return 0;
}

// Create a new process copying p as the parent.
// Sets up stack to return as if from system call.
// Caller must set state of returned proc to RUNNABLE.
int
fork(void)
{
  int i, pid;
  struct proc *np;

  // Allocate process.
  if((np = allocproc()) == 0)
    return -1;

  // Copy process state from p.
  if((np->pgdir = copyuvm(proc->pgdir, proc->sz)) == 0){
    kfree(np->kstack);
    np->kstack = 0;
    np->state = UNUSED;
    return -1;
  }
  np->sz = proc->sz;
  np->parent = proc;
  *np->tf = *proc->tf;

/***************************/
	//Copy the parent's tickets and nice values into the child
	setTicketsNice(np, MaxRand(1) % proc->tickets, proc->nice);

/***************************/

  // Clear %eax so that fork returns 0 in the child.
  np->tf->eax = 0;

  for(i = 0; i < NOFILE; i++)
    if(proc->ofile[i])
      np->ofile[i] = filedup(proc->ofile[i]);
  np->cwd = idup(proc->cwd);

  safestrcpy(np->name, proc->name, sizeof(proc->name));
 
  pid = np->pid;

  // lock to force the compiler to emit the np->state write last.
  acquire(&ptable.lock);
  np->state = RUNNABLE;
  release(&ptable.lock);
  
  return pid;
}

// Exit the current process.  Does not return.
// An exited process remains in the zombie state
// until its parent calls wait() to find out it exited.
void
exit(void)
{
  struct proc *p;
  int fd;

  if(proc == initproc)
    panic("init exiting");

  // Close all open files.
  for(fd = 0; fd < NOFILE; fd++){
    if(proc->ofile[fd]){
      fileclose(proc->ofile[fd]);
      proc->ofile[fd] = 0;
    }
  }

  begin_op();
  iput(proc->cwd);
  end_op();
  proc->cwd = 0;

  acquire(&ptable.lock);

  // Parent might be sleeping in wait().
  wakeup1(proc->parent);

  // Pass abandoned children to init.
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
    if(p->parent == proc){
      p->parent = initproc;
      if(p->state == ZOMBIE)
        wakeup1(initproc);
    }
  }

  // Jump into the scheduler, never to return.
  proc->state = ZOMBIE;
  sched();
  panic("zombie exit");
}

// Wait for a child process to exit and return its pid.
// Return -1 if this process has no children.
int
wait(void)
{
  struct proc *p;
  int havekids, pid;

  acquire(&ptable.lock);
  for(;;){
    // Scan through table looking for zombie children.
    havekids = 0;
    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
      if(p->parent != proc)
        continue;
      havekids = 1;
      if(p->state == ZOMBIE){
        // Found one.
        pid = p->pid;
        kfree(p->kstack);
        p->kstack = 0;
        freevm(p->pgdir);
        p->state = UNUSED;
        p->pid = 0;

	/******************/
	AllTickets -= p->tickets;

        p->parent = 0;
        p->name[0] = 0;
        p->killed = 0;
        release(&ptable.lock);
        return pid;
      }
    }

    // No point waiting if we don't have any children.
    if(!havekids || proc->killed){
      release(&ptable.lock);
      return -1;
    }

    // Wait for children to exit.  (See wakeup1 call in proc_exit.)
    sleep(proc, &ptable.lock);  //DOC: wait-sleep
  }
}

//PAGEBREAK: 42
// Per-CPU process scheduler.
// Each CPU calls scheduler() after setting itself up.
// Scheduler never returns.  It loops, doing:
//  - choose a process to run
//  - swtch to start running that process
//  - eventually that process transfers control
//      via swtch back to the scheduler.
void
scheduler_b(void)
{
  struct proc *p;
  int foundproc = 1;

  for(;;){
    // Enable interrupts on this processor.
    sti();

    if (!foundproc) hlt();

    foundproc = 0;

    // Loop over process table looking for process to run.
    acquire(&ptable.lock);
    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
      if(p->state != RUNNABLE)
        continue;

      // Switch to chosen process.  It is the process's job
      // to release ptable.lock and then reacquire it
      // before jumping back to us.
      foundproc = 1;
      proc = p;
      switchuvm(p);
      p->state = RUNNING;
      swtch(&cpu->scheduler, proc->context);
      switchkvm();

      // Process is done running for now.
      // It should have changed its p->state before coming back.
      proc = 0;
    }
    release(&ptable.lock);

  }
}

int CalculateMax(void)
{
	struct proc *pp;
	int MAXNUM = 0;
	for(pp = ptable.proc; pp < &ptable.proc[NPROC]; pp++){
      		if(pp->state != RUNNABLE)
        	continue;
	if(pp->tickets <= 0)
	{
		cprintf("ERROR:  PROCESS HAS INSUFFICIENT TICKETS\n");
		continue;
	}

	MAXNUM += pp->tickets;
	}

	return MAXNUM;
}

int DistributeTickets(void)
{
	struct proc *p;
	int MAXTICKETS = 0;

    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
      if(p->state != RUNNABLE)
        continue;

/*****  GIVE EVERY PROCESS A RANDOM NICE VALUE ****/

      /*******************************/
      /* Generate random ticket */
      int ticket = 0;
      while(p->nice < 1)			//No Nice Value assigned, give it a random one
      {
	p->nice = MaxRand(20) + 1;	//Mod 0 crashes everything, 1 will be the minimum  
      }
      if(p->tickets <= 1)
      {
	ticket = MaxRand(CalculateMax()) % p->nice;
      }

	p->tickets = ticket+1;		//Adding +1 because ticket = 0 breaks the scheduler
	MAXTICKETS += p->tickets;

      /*****************************************/
    }
	return MAXTICKETS;
}

void setTicketsNice(struct proc *p, int ticket, int NewNice)
{
	if(ticket == 0)
		ticket++;
	else if(ticket < 0)
		ticket = ticket * -1;

	AllTickets -= p->tickets;
	p->tickets = ticket;
	p->nice = NewNice;
	AllTickets += p->tickets;
}

void scheduler(void)
{
  struct proc *p;
  int ticket_counter = 0;
  int MAXTICKET = 0;

  int foundproc = 1;
    //This function must not be interrupted during execution.


  for(;;){
    // Enable interrupts on this processor.
    sti();

    if (!foundproc) hlt();

    foundproc = 0;
    // Loop over process table looking for process to run.
    acquire(&ptable.lock);

    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
      if(p->state != RUNNABLE)
        continue;

      // Switch to chosen process.  It is the process's job
      // to release ptable.lock and then reacquire it
      // before jumping back to us.
      foundproc = 1;
      proc = p;
      switchuvm(p);

    AllTickets = DistributeTickets();			//Distribute to each process.
    int Winning_Ticket = MaxRand(1) % (MAXTICKET + 1);

	/**********GENERATE WINNING TICKET*************/
	    MAXTICKET = CalculateMax();
	    //cprintf("Maxticket:  %d\n", MAXTICKET);
	    do{
	    Winning_Ticket = MaxRand(0) % (MAXTICKET);
	    }while(Winning_Ticket > MAXTICKET);

		//cprintf("Winning Ticket:  %d\n", Winning_Ticket);

	/***********GENERATE WINNING TICKET************/

/**********FIND THE CHOSEN PROCESS*******************/

	if(p->nice <= 0)
		cprintf("ERROR:  UNIDENTIFIED NICE VALUE\n");

	//Find the process with the winning ticket
	//Dividing by p->nice as a form of priority.  Higher nice values means the tickets weight less.
	if((ticket_counter + p->tickets / p->nice) < Winning_Ticket)
	{
		int temp = p->tickets;
			////This in addition to dividing ticket_counter by p->nice leads to out of bounds errors

		//Not the chosen one, mark this as ignored and move on
		p->ignored++;			//Increment the ignored counter
		if(p->ignored > 3 && p->nice > 1)
		{
			//Ignored too many times, increase priority and reset the counter
			p->nice--;			
			//AlterNice(p, p->nice-1);			//Increase priority and give it a new set of tickets.
			p->ignored = 0;
		}

//Leads to panic errors
		else if(p->ignored > 5)
		{
			AllTickets -= temp;
			AllTickets += p->tickets;
			p->nice = MaxRand(20) + 2;
			p->ignored = 0;
		}


		ticket_counter += temp;
		continue;
	}
	if(DEBUG)
	{
		cprintf("MAXTICKET:  %d\n", CalculateMax());
		cprintf("PID:  %d has been chosen\t Has a ticket of %d\t winning ticket: %d\t nice: %d\n", p->pid, ticket_counter+p->tickets, Winning_Ticket, p->nice);
	}

	ticket_counter = 0;
/*****************************/
      p->state = RUNNING;
      swtch(&cpu->scheduler, proc->context);
      switchkvm();

      // Process is done running for now.
      // It should have changed its p->state before coming back.
      proc = 0;
/****************************/
    }
    release(&ptable.lock);
  }
}


// Enter scheduler.  Must hold only ptable.lock
// and have changed proc->state.
void
sched(void)
{
  int intena;

  if(!holding(&ptable.lock))
    panic("sched ptable.lock");
  if(cpu->ncli != 1)
    panic("sched locks");
  if(proc->state == RUNNING)
    panic("sched running");
  if(readeflags()&FL_IF)
    panic("sched interruptible");
  intena = cpu->intena;
  swtch(&proc->context, cpu->scheduler);
  cpu->intena = intena;
}

// Give up the CPU for one scheduling round.
void
yield(void)
{
  acquire(&ptable.lock);  //DOC: yieldlock
  proc->state = RUNNABLE;
  sched();
  release(&ptable.lock);
}

// A fork child's very first scheduling by scheduler()
// will swtch here.  "Return" to user space.
void
forkret(void)
{
  static int first = 1;
  // Still holding ptable.lock from scheduler.
  release(&ptable.lock);

  if (first) {
    // Some initialization functions must be run in the context
    // of a regular process (e.g., they call sleep), and thus cannot 
    // be run from main().
    first = 0;
    iinit(ROOTDEV);
    initlog(ROOTDEV);
  }
  
  // Return to "caller", actually trapret (see allocproc).
}

// Atomically release lock and sleep on chan.
// Reacquires lock when awakened.
void
sleep(void *chan, struct spinlock *lk)
{
  if(proc == 0)
    panic("sleep");

  if(lk == 0)
    panic("sleep without lk");

  // Must acquire ptable.lock in order to
  // change p->state and then call sched.
  // Once we hold ptable.lock, we can be
  // guaranteed that we won't miss any wakeup
  // (wakeup runs with ptable.lock locked),
  // so it's okay to release lk.
  if(lk != &ptable.lock){  //DOC: sleeplock0
    acquire(&ptable.lock);  //DOC: sleeplock1
    release(lk);
  }

  // Go to sleep.
/*************************/
	//Will cause a panic trap error

	//Take this processor's tickets out of the queue
	//cprintf("Proc tickets: %d\n", proc->tickets);
	//cprintf("AllTickets: %d\n", AllTickets);
	//AllTickets -= proc->tickets;
/*************************/

  proc->chan = chan;
  proc->state = SLEEPING;
  sched();

  // Tidy up.
  proc->chan = 0;

  // Reacquire original lock.
  if(lk != &ptable.lock){  //DOC: sleeplock2
    release(&ptable.lock);
    acquire(lk);
  }
}

//PAGEBREAK!
// Wake up all processes sleeping on chan.
// The ptable lock must be held.
static void
wakeup1(void *chan)
{
  struct proc *p;

  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++)
    if(p->state == SLEEPING && p->chan == chan)
	{

/*****************/
	//Restore ticket counter to the list
	AllTickets += p->tickets;
/*****************/

      p->state = RUNNABLE;
	}
}

// Wake up all processes sleeping on chan.
void
wakeup(void *chan)
{
  acquire(&ptable.lock);
  wakeup1(chan);
  release(&ptable.lock);
}

// Kill the process with the given pid.
// Process won't exit until it returns
// to user space (see trap in trap.c).
int
kill(int pid)
{
  struct proc *p;

  acquire(&ptable.lock);
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
    if(p->pid == pid){
      p->killed = 1;

	/**********TAKE OUT THE PROCESSOR FROM THE SCHEDULER****************/
	AllTickets -= p->tickets;
	p->nice = 0;
	p->tickets = 0;
	/********TAKE OUT THE TICKETS FROM THE TICKET COUNTER***************/

      // Wake process from sleep if necessary.
      if(p->state == SLEEPING)
        p->state = RUNNABLE;
      release(&ptable.lock);
      return 0;
    }
  }
  release(&ptable.lock);
  return -1;
}

//PAGEBREAK: 36
// Print a process listing to console.  For debugging.
// Runs when user types ^P on console.
// No lock to avoid wedging a stuck machine further.
void
procdump(void)
{
  static char *states[] = {
  [UNUSED]    "unused",
  [EMBRYO]    "embryo",
  [SLEEPING]  "sleep ",
  [RUNNABLE]  "runble",
  [RUNNING]   "run   ",
  [ZOMBIE]    "zombie"
  };
  int i;
  struct proc *p;
  char *state;
  uint pc[10];
  
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
    if(p->state == UNUSED)
      continue;
    if(p->state >= 0 && p->state < NELEM(states) && states[p->state])
      state = states[p->state];
    else
      state = "???";
    cprintf("%d %s %s %d", p->pid, state, p->name, p->tickets);
    if(p->state == SLEEPING){
      getcallerpcs((uint*)p->context->ebp+2, pc);
      for(i=0; i<10 && pc[i] != 0; i++)
        cprintf(" %p", pc[i]);
    }
    cprintf("\n");
  }
}

//The one used by Task 1 of the homework 3.
int ChangeNice(int pid, int NewNice)
{
	//Must check the entire process table
	struct proc *p;
	for(p = ptable.proc; p < &ptable.proc[NPROC]; p++)
	{
		if(p->pid == pid)
		{
			p->nice = NewNice;		//Assign a new priority value

			//Randomize ticket value
			AllTickets -= p->tickets;
			p->tickets = MaxRand(1) % p->nice + 1;
			AllTickets += p->tickets;
			break;
		}
	}


	if(DEBUG)
		cprintf("Pid %d, Nice:  %d\n", p->pid, p->nice);

	return NewNice;
}

//The one used by the scheduler itself
void AlterNice(struct proc *p, int NewNice)
{
	if(NewNice < 2)
	{
		NewNice = MaxRand(20);
	}

	AllTickets -= p->tickets;		//Take out the old ticket value
	p->nice = NewNice;			//Assign a new priority value
	p->tickets = ((ReturnXor(2* AllTickets + p->tickets, 0) % 100) / p->nice) + 1;	//Because priority is being changed, reassign it another set of tickets
	AllTickets += p->tickets;		//Add in the new ticket value
}

int cps(void)
{
	
	//cprintf("AllTickets:  %d\n", CalculateMax());
	//Must check the entire process table
	struct proc *p;
	for(p = ptable.proc; p < &ptable.proc[NPROC]; p++)
	{
		if(p->pid != 0)
		{
		 cprintf("PID:  %d,  Nice:  %d,  Tickets:  %d\n", p->pid, p->nice, p->tickets);
		}
	}
	return -1;
}