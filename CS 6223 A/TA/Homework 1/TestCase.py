from utils import register_test, register_build, exec_as_student
from utils import (
    TestResult, BuildResult, Panic, DEBUG,
    xv6_run, did_xv6_crash,
    verify_expected, search_lines, test_lines
)

@register_build
def build(build_result: BuildResult):
    stdout, retcode = exec_as_student('make xv6.img fs.img')

    build_result.stdout = stdout.decode()
    build_result.passed = retcode == 0

@register_test('test hello.c')
def test_1(test_result: TestResult):
    test_result.stdout = "Executing hello\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("hello", test_result)

    # Run hello as student user and capture output lines
    expected_raw, _ = exec_as_student('hello')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)

@register_test('test uniq.c')
def test_2(test_result: TestResult):
    test_result.stdout = "Executing uniq example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("uniq example.txt", test_result)

    # Run uniq example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('uniq example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test uniq -c example.txt')
def test_3(test_result: TestResult):
    test_result.stdout = "Executing uniq -c example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("uniq -c example.txt", test_result)

    # Run uniq -c example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('uniq -c example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test uniq -d example.txt')
def test_4(test_result: TestResult):
    test_result.stdout = "Executing uniq -d example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("uniq -d example.txt", test_result)

    # Run uniq -d example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('uniq -d example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test uniq -i example.txt')
def test_5(test_result: TestResult):
    test_result.stdout = "Executing uniq -i example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("uniq -i example.txt", test_result)

    # Run uniq -i example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('uniq -i example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test uniq -d -i example.txt')
def test_6(test_result: TestResult):
    test_result.stdout = "Executing uniq -d -i example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("uniq -d -i example.txt", test_result)

    # Run uniq -d -i example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('uniq -d -i example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test uniq -c -i example.txt')
def test_7(test_result: TestResult):
    test_result.stdout = "Executing uniq -c -i example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("uniq -c -i example.txt", test_result)

    # Run uniq -c -i example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('uniq -c -i example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test cat example.txt | uniq example.txt')
def test_8(test_result: TestResult):
    test_result.stdout = "Executing cat example.txt | uniq example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("cat example.txt | uniq example.txt", test_result)

    # Run cat example.txt | uniq example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('cat example.txt | uniq example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test cat example.txt | uniq -c example.txt')
def test_9(test_result: TestResult):
    test_result.stdout = "Executing cat example.txt | uniq -c example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("cat example.txt | uniq -c example.txt", test_result)

    # Run cat example.txt | uniq -c example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('cat example.txt | uniq -c example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test cat example.txt | uniq -i example.txt')
def test_10(test_result: TestResult):
    test_result.stdout = "Executing cat example.txt | uniq -i example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("cat example.txt | uniq -i example.txt", test_result)

    # Run cat example.txt | uniq -i example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('cat example.txt | uniq -i example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test cat example.txt | uniq -i example.txt')
def test_11(test_result: TestResult):
    test_result.stdout = "Executing cat example.txt | uniq -i example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("cat example.txt | uniq -i example.txt", test_result)

    # Run cat example.txt | uniq -i example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('cat example.txt | uniq -i example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test cat example.txt | uniq -c -i example.txt')
	
def test_12(test_result: TestResult):
    test_result.stdout = "Executing cat example.txt | uniq -d example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("cat example.txt | uniq -d example.txt", test_result)

    # Run cat example.txt | uniq -i example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('cat example.txt | uniq -d example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test cat example.txt | uniq -c -i example.txt')

def test_13(test_result: TestResult):
    test_result.stdout = "Executing cat example.txt | uniq -c -i example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("cat example.txt | uniq -c -i example.txt", test_result)

    # Run cat example.txt | uniq -c -i example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('cat example.txt | uniq -c -i example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)
	
	@register_test('test cat example.txt | uniq -d -i example.txt')
def test_14(test_result: TestResult):
    test_result.stdout = "Executing cat example.txt | uniq -d -i example.txt\n"

    # Start xv6 and run command
    stdout_lines = xv6_run("cat example.txt | uniq -d -i example.txt", test_result)

    # Run cat example.txt | uniq -d -i example.txt as student user and capture output lines
    expected_raw, _ = exec_as_student('cat example.txt | uniq -d -i example.txt')
    expected = expected_raw.decode().strip().split('\n')

    # Attempt to detect crash
    if did_xv6_crash(stdout_lines, test_result):
        return

    # Test to see if the expected result was found
    verify_expected(stdout_lines, expected, test_result)