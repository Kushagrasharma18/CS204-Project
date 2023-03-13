# RISC-V-Simulator

This is the repository for the RISC-V simulator code.
This is the final project for the course CS-204 - Computer Architecture.

<br> 
The team members are:
<br>

1. <p style="color:#EA8FEA;"> Vavadiya Harsh </p>
2. <p style="color:#EA8FEA;"> Ayush Sahu lodu </p>
3. <p style="color:#EA8FEA;"> Kushagra Sharma </p>
4. <p style="color:#FFF4D2;"> Patel Het </p>

<br>
The simulator is written in cpp.

<br>

### Testing the simulator
To test the simulator, add a `.mc` file containing addresses of each instruction followed by the machine code of each instruction (or you can just write the machine code, and the code automatically give the address to the machine code, 0x0 to first instruction, 0x4 to second instruction and so on..) and run the program as described below. Example below

```
0X0 0X00A00093
0X4 0X00900113
0X8 0X002081B3
0XC 0X004000EF
0X10 0X00000263
0X14 0X0202423
0X18 0X00802283

OR

0X00A00093
0X00900113
0X002081B3
0X004000EF
0X00000263
0X0202423
0X00802283
```
## Running the simulator
For running the code, in the file "myRISVsim.h" we have to comment and uncomment the part of function load_program_memory() depending upon the type of input. Just clone the repository and run the myRISVsim.cpp. (Also make sure you have some C compiler installed.) 

<br>

This will create 3 output files (MEM_out.mem,INS_OUT.mem and Registor_out.mem) which represents the memory , instuctions runs and final registor values respectively.

<br>

If you want to run the code by step, the uncomment the portion of the function run_riscvsim() in the file "myRISVsim.h".
