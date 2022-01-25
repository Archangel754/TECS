# TECS
TECS Jack Compiler for compiling Jack code to run on the HACK hardware design.

TECS Jack Compiler is a compiler for the simple object-based language Jack designed to run on the HACK hardware platform. The code is compiled in three stages. First the CompilationEngine module compiles Jack code into virtual machine (VM) code. The VMtranslator module then compiles the VM code into HACK assembly language (asm). The assembler module translates the assembly language into machine code which runs on the HACK hardware. The simple HACK computer was designed from NAND gates up to a full computer including CPU and memory units. The HACK hardware is simulated on software tools provided by Nisan and Schocken (https://www.nand2tetris.org/).  

**Instructions:**  
The compiler is written entirely in Python, and requires version 3.10.  
Each component of the compiler may be used by itself to compile one stage at a time. However, the simplest method is to use the JackCompiler.py file to perform all the steps at once.  
JackCompiler.py can be called from the command line. It should be passed one argument which is the name of a folder containing the .jack files to be compiled. The folder should also contain any OS .vm files, containing functions referenced in the Jack code. 


**Example:**  
**./JackCompiler.py Sum/**  

Following is an sample of code at each stage of the process. As simple functions compile into many lines of VM code and hundreds or thousands of assembly instructions, only small snippets are shown here to demonstrate the format of the output.  

**/Sum/Main.jack:**
```
// Computes and prints the sum of two numbers
class Main {
    function void main() {
        var int a, b;

        let a = Keyboard.readInt("Enter first number: ");
        let b = Keyboard.readInt("Enter second number: ");

        do Output.printString("The sum is ");
        do Output.printInt(a+b);
        return;
    }
}
```

**/Sum/Main.vm abbreviated:**
```
function Main.main 2
push constant 20
call String.new 1
push constant 69
call String.appendChar 2
push constant 110
...
call Output.printString 1
pop temp 0
push local 0
push local 1
add
call Output.printInt 1
pop temp 0
push constant 0
return
```

**/Sum.asm code snippet:**
```
...
(returnaddressfrom.String.appendChar277)
@115
D=A
@SP
A=M 
M=D
@SP
M=M+1
@returnaddressfrom.String.appendChar278
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
...
```

**/Sum.hack code snippet:**
```
...
0000000100000000
1110110000010000
0000000000000000
1110001100001000
0000000000110011
1110110000010000
0000000000000000
1111110000100000
1110001100001000
0000000000000000
1111110111001000
0000000000000001
1111110000010000
0000000000000000
1111110000100000
...
```