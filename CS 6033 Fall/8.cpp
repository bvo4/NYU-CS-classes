Build(T, A)
For i = 0 to A.length
//It takes O(log n) time to insert 1 node.
//We have to insert n nodes each, making it cost O(n log n) time to insert every element in an array into a tree
	INSERT(T, A[i])		//Insert new subscriber
EndFor

Local_Subscriber_List(T, zipcode)
//Find a list of all subscribers in the area who share the same zipcode
Create array S
While (T.node != nil)	//Would require O(log n) time to travel down a BST tree to find the 
//subtree where subscribers  with the same zip code would be found
	If (T.zipcode == zipcode)
//Use a loop that will go down the subtree and return the list of subscribers
//The process to go through each list of subscribers S in a list would be O(S)
		Traverse_ZIP(T, zipcode)
	Else If (zipcode > T.zipcode)	T = T.right
	Else	T = T.left
EndWhile

Traverse-Zip(T, zipcode)
	If (T.zipcode == zipcode or T.value != nil)	//Recursively travel down the subtree and print 
// out the subscriber’s name. 
//Repeat this process for as long as we keep finding matching zipcodes or until we reach an empty node
//Because the data tree will focus on keeping every subscriber holding the same zipcode in the same 
//subtree, this will take approximately O(S) time to find every subscriber with the same zipcode because 
//we will be travelling down one subtree until we no longer find a match then exit out.
		Print T.subscriber_name
		Traverse-Zip(T.left, zipcode)
		Traverse-Zip(T.right, zipcode)
	Else
		Return	//Exit out of function

Insert(T, s)	//Insert a new subscriber into the tree
Y = T.nil
X = T.root
While (s != T.Nil)		//Go down the tree until we reach an empty nil node.
	Y = X
	If (s.zipcode < T.zipcode)
		X = X.left
	Else if (s.zipcode > T.zipcode)
		X = X.right
	Else (s.zipcode == T.zipcode)
		If (s.subscriber_name < T.subscriber_name)
			If(T.left.zipcode != T.zipcode)
				If (T.left.subscriber_name < s.subscriber_name)
					//Insert S as the left child
					T.left.p = S
					S.p = T
					S.left = T.left
			Else // (T.right.zipcode != T.zipcode)
				If (T.right.subscriber_name > s.subscriber_name)
					T.right.p = S
					S.p = T
					S.right = T.right
					 
EndLoop
z.p = y
If y == T.nil
	T.root = z
Else if z.key < y.key
	y.left = z
else y.right = z
z.left = T.nil
z.right = T.nil
z.color = Red
RB-INSERT-FIXUP(T, z)