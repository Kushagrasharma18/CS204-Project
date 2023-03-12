/*

The project is developed as part of Computer Architecture class
Project Name: Functional Simulator for subset of ARM Processor

Developer's Name:
Developer's Email id:
Date:

*/

/* myRISCVSim.h
   Purpose of this file: header file for myARMSim
*/

/*

The project is developed as part of Computer Architecture class
Project Name: Functional Simulator for subset of RISCV Processor

Developer's Name:
Developer's Email id:
Date:

*/

/* myRISCVSim.cpp
   Purpose of this file: implementation file for myRISCVSim
*/

#include <bits/stdc++.h>
#include <iostream>
#include <stdlib.h>
// #include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
using namespace std;
// Register file
static int X[32];
// flags
// memory
static unsigned char MEM[4000];
static int IR;
static unsigned int PC = 0x00000000;
static int stackPointer = 4000;
// intermediate datapath and control path signals
// static unsigned int instruction_word;
static unsigned int operand1;
static unsigned int operand2;
static unsigned int control;
static unsigned int cycle;
static int imm;
static int Rs1;
static int Rs2;
static int Rd;
static int Rz;
static int Ry;
static int Rm;
static int temp_PC;
static int opcode;
static int error = 0;
FILE *filePointer;
clock_t clock_time;

// it is used to set the reset values
// reset all registers and memory content to 0
int read_word(unsigned char *mem, unsigned int address)
{
  int *data;
  data = (int *)(mem + address);
  return *data;
}

void write_word(unsigned char *mem, unsigned int address, unsigned int data)
{
  int *data_p;
  data_p = (int *)(mem + address);
  *data_p = data;
}


void reset_proc()
{
  for (int i = 0; i < 32; i++)
  {
    X[i] = 0x00000000;
  }
  X[2] = stackPointer;
  for (int i = 0; i < 4000; i++)
  {
    MEM[i] = 0x00000000;
  }
}

// load_program_memory reads the input memory, and pupulates the instruction
//  memory
void load_program_memory()
{
  FILE *fp;
  unsigned int address = 0, instruction;
  fp = fopen("machineCode.mc", "r");

  if (fp == NULL)
  {
    printf("Error opening input mem file\n");
    exit(1);
  }

  while (fscanf(fp, "%x", &instruction) != EOF)
  {
    write_word(MEM, address, instruction);
    address += 4;
  }

  // while (fscanf(fp, "%x %x",&address, &instruction) != EOF)
  // {
  //   write_word(MEM, address, instruction);
  // }

  fclose(fp);

  for (int i = 0; i < 32; i++)
  {
    X[i] = 0x00000000;
  }

  X[2] = stackPointer;
}

// writes the data memory in "data_out.mem" file
void write_data_memory()
{
  FILE *fp;
  unsigned int i;
  fp = fopen("MEM_out.mem", "w");

  if (fp == NULL)
  {
    printf("Error opening MEM_out.mem file for writing\n");
    return;
  }

  for (i = 0; i < 4000; i = i + 4)
  {
    fprintf(fp, "0x%x 0x%x (%d)\n", i, read_word(MEM, i), read_word(MEM, i));
  }
  fclose(fp);

  fp = fopen("Registor_out.mem", "w");

  if (fp == NULL)
  {
    printf("Error opening Registor_out.mem file for writing\n");
    return;
  }

  for (i = 0; i < 32; i++)
  {

    fprintf(fp, "X%d : 0x%x (%d)\n", i, X[i], X[i]);
  }
  fclose(fp);
}

// should be called when instruction is swi_exit
void swi_exit()
{
  write_data_memory();
  filePointer = fopen("INS_OUT.mem", "a");
  fprintf(filePointer, "=====FINISH=====\n");
  fclose(filePointer);
  cout << "Cycles: " << cycle << endl;
  cout << "Errors: " << error << endl;
  clock_time = clock() - clock_time;
  cout << "Time Taken: " << (float)clock_time / CLOCKS_PER_SEC << endl;
  exit(0);
}

// reads from the instruction memory and updates the instruction register
void fetch()
{
  IR = read_word(MEM, PC);
  if (IR == 0xffffffff)
  {
    swi_exit();
  }
  // Increment the program counter
  PC += 4;
}


//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DECODE STARTS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

// reads the instruction register, reads operand1, operand2 fromo register file, decides the operation to be performed in execute stage
int op_code(int i)
{
  int temp = 0;
  temp = (i & 0x7f);
  return temp;
}


int imm_i(int i)
{
  int temp = 0;

  temp |= (i >> 20);
  return temp;
}


int imm_s(int i)
{
  int temp = 0x00000000;
  temp = ((i >> 7) & 0x1F);
  temp |= ((i >> 25) << 5);
  return temp;
}


int imm_b(int i)
{
  int temp = 0;
  temp |= (((i >> 31)) << 12);       // imm[12]
  temp |= (((i >> 7) & 0x1) << 11);  // imm[11]
  temp |= (((i >> 25) & 0x3f) << 5); // imm[10:5]
  temp |= (((i >> 8) & 0xf) << 1);   // imm[4:1]
  return temp;
}


int imm_u(int i)
{
  int temp = 0;
  temp = i & 0xfffff000;
  return temp;
}


int imm_j(int i)
{
  int temp = 0;
  temp |= (((i >> 31)) << 20);        // imm[20]
  temp |= (((i >> 12) & 0xff) << 12); // imm[19:12]
  temp |= (((i >> 20) & 0x1) << 11);  // imm[11]
  temp |= (((i >> 21) & 0x3ff) << 1); // imm[10:1]
  return temp;
}


int func_7(int i)
{
  int temp = 0;
  temp = (i >> 25);
  return temp;
}


int func_3(int i)
{
  int temp = 0;
  temp = (i >> 12) & 0x7;
  return temp;
}


int r_s_1(int i)
{
  int temp = 0;
  temp = (i >> 15) & 0x1f;
  return temp;
}


int r_s_2(int i)
{
  int temp = 0;
  temp = (i >> 20) & 0x1f;
  return temp;
}


int r_d(int i)
{
  int temp = 0;
  temp = (i >> 7) & 0x1f;
  return temp;
}


void r_type(int i)
{
  Rs1 = X[r_s_1(i)];
  Rs2 = X[r_s_2(i)];
  int funct3 = func_3(i);
  int funct7 = func_7(i);
  Rd = r_d(i);
  // cout << "Rs1 " << Rs1 << " " << r_s_1(i) << "Rs2 " << Rs2 << " " << r_s_2(i) << "f3 " << funct3 << "f7 " << funct7 << "Rd " << Rd << endl;
  switch (funct3)
  {
  case 0:
    switch (funct7)
    {
    case 0: // ADD

      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:ADD X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
      fclose(filePointer);
      control = 1;
      break;

    case 32: // SUB
      control = 2;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:SUB X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
      fclose(filePointer);
      break;

    default:
      cout << "Wrong function 7 value" << endl;
      error++;
      break;
    }
    break;

  case 1: // sll
    control = 3;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:SLL X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  case 2: // slt
    control = 4;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:SLT X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  case 4: // xor
    control = 5;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:XOR X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  case 5:

    switch (funct7)
    {
    case 0: // srl
      control = 6;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:SRL X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
      fclose(filePointer);
      break;

    case 32: // sra
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:SRA X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
      fclose(filePointer);
      break;

    default:
      cout << "Wrong function 7 value" << endl;
      error++;
      break;
    }
    break;

  case 6: // or
    control = 8;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:OR X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  case 7: // AND
    control = 9;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:AND X%d X%d X%d #X%d=%d , X%d=%d\n", Rd, r_s_1(i), r_s_2(i), r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  default:
    cout << "Wrong function 3 value" << endl;
    error++;
    break;
  }
}


void i_type(int i)
{
  imm = imm_i(i);
  Rs1 = X[r_s_1(i)];
  int funct3 = func_3(i);
  Rd = r_d(i);
  int opc = op_code(i);

  if (opc == 19)
  {
    switch (funct3)
    {
    case 0: // addi
      control = 10;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:ADDI X%d X%d %d #X%d=%d \n", Rd, r_s_1(i), imm, r_s_1(i), Rs1);
      fclose(filePointer);
      break;

    case 6: // ori
      control = 11;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:ORI X%d X%d %d #X%d=%d \n", Rd, r_s_1(i), imm, r_s_1(i), Rs1);
      fclose(filePointer);
      break;

    case 7: // andi
      control = 12;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:ANDI X%d X%d %d #X%d=%d \n", Rd, r_s_1(i), imm, r_s_1(i), Rs1);
      fclose(filePointer);
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      error++;
      break;
    }
  }
  else if (opc == 3)
  {
    switch (funct3)
    {
    case 0: // lb
      control = 13;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:LB X%d  %d(X%d) #X%d=%d \n", Rd, imm, r_s_1(i), r_s_1(i), Rs1);
      fclose(filePointer);
      break;

    case 1: // lh
      control = 14;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:LH X%d  %d(X%d) #X%d=%d \n", Rd, imm, r_s_1(i), r_s_1(i), Rs1);
      fclose(filePointer);
      break;

    case 2: // lw
      control = 15;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "INS:LW X%d  %d(X%d) #X%d=%d \n", Rd, imm, r_s_1(i), r_s_1(i), Rs1);
      fclose(filePointer);
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      error++;
      break;
    }
  }
  else
  {
    control = 16; // jalr
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:JALR X%d X%d %d #X%d=%d \n", Rd, r_s_1(i), imm, r_s_1(i), Rs1);
    fclose(filePointer);
  }
}


void s_type(int i)
{
  imm = imm_s(i);
  Rs2 = X[r_s_2(i)];
  Rs1 = X[r_s_1(i)];
  int funct3 = func_3(i);

  switch (funct3)
  {
  case 0x0: // sb
    control = 17;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:SB X%d  %d(X%d) #X%d=0x%x \n", Rd, imm, r_s_1(i), r_s_1(i), Rs1);
    fclose(filePointer);
    break;

  case 0x1: // sh
    control = 18;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:SH X%d  %d(X%d) #X%d=0x%x \n", Rd, imm, r_s_1(i), r_s_1(i), Rs1);
    fclose(filePointer);
    break;

  case 0x2: // sw
    control = 19;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:SW X%d  %d(X%d) #X%d=0x%x \n", Rd, imm, r_s_1(i), r_s_1(i), Rs1);
    fclose(filePointer);
    break;

  default:
    cout << "Wrong function 3 value" << endl;
    error++;
    break;
  }
}


void b_type(int i)
{
  imm = imm_b(i);
  Rs2 = X[r_s_2(i)];
  Rs1 = X[r_s_1(i)];
  int funct3 = func_3(i);
  switch (funct3)
  {
  case 0x0: // beq
    control = 20;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:BEQ X%d X%d 0x%x #X%d=%d,X%d=%d \n", r_s_1(i), r_s_2(i), imm, r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  case 0x1: // bne
    control = 21;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:BNE X%d X%d 0x%x #X%d=%d,X%d=%d \n", r_s_1(i), r_s_2(i), imm, r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  case 0x4: // blt
    control = 22;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:BLT X%d X%d 0x%x #X%d=%d,X%d=%d \n", r_s_1(i), r_s_2(i), imm, r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  case 0x5: // bge
    control = 23;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:BGE X%d X%d 0x%x #X%d=%d,X%d=%d \n", r_s_1(i), r_s_2(i), imm, r_s_1(i), Rs1, r_s_2(i), Rs2);
    fclose(filePointer);
    break;

  default:
    cout << "Wrong function 3 value" << endl;
    error++;
    break;
  }
}


void u_type(int i)
{
  imm = imm_u(i);
  Rd = r_d(i);
  int opc = op_code(i);
  // cout << "I " << imm << " Rd " << Rd << " " << endl;
  if (opc == 55)
  {
    control = 24; // lui

    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:LUI X%d  0x%x\n", Rd, imm);
    fclose(filePointer);
  }
  else
  {
    control = 25; // auipc
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "INS:AUIPC X%d  0x%x\n", Rd, imm);
    fclose(filePointer);
  }
}


void j_type(int i)
{
  imm = imm_j(i);
  Rd = r_d(i);
  control = 26; // jal
  filePointer = fopen("INS_OUT.mem", "a");
  fprintf(filePointer, "INS:JAL X%d  0x%x\n", Rd, imm);
  fclose(filePointer);
  // cout << "I " << imm << " Rd " << Rd << " " << endl;
}


void decode()
{
  opcode = op_code(IR); // Extract opcode
  if (opcode == 51)
  {
    r_type(IR);
  }
  else if (opcode == 19 || opcode == 3 || opcode == 103)
  {
    i_type(IR);
  }
  else if (opcode == 35)
  {
    s_type(IR);
  }
  else if (opcode == 99)
  {
    b_type(IR);
  }
  else if (opcode == 55 || opcode == 23)
  {
    u_type(IR);
  }
  else if (opcode == 111)
  {
    j_type(IR);
  }
  else
  {
    cout << "Wrong OPcode!!\n"
         << endl;
    error++;
  }
}




// executes the ALU operation based on ALUop
void execute()
{
  switch (control)
  {
  case 1:
    Rz = Rs1 + Rs2; // ADD
    break;

  case 2:
    Rz = Rs1 - Rs2; // SUB
    break;

  case 3:

    Rz = Rs1 << Rs2; // SLL

    break;

  case 4:
    Rz = (Rs1 < Rs2) ? 1 : 0; // SLT
    break;

  case 5:
    Rz = Rs1 ^ Rs2; // XOR
    break;

  case 6:
    Rz = (int)((unsigned int)Rs1 >> Rs2); // SRL
    break;

  case 7:
    Rz = Rs1 >> Rs2; // SRA
    break;

  case 8:
    Rz = Rs1 | Rs2; // OR
    break;

  case 9:
    Rz = Rs1 & Rs2; // AND
    break;

  case 10:
    Rz = Rs1 + imm; // ADDI
    break;

  case 11:
    Rz = Rs1 | imm; // ORI
    break;

  case 12:
    Rz = Rs1 & imm; // ADDI
    break;

  case 13:
    Rz = Rs1 + imm; // LB
    break;

  case 14:
    Rz = Rs1 + imm; // LH
    break;

  case 15:
    Rz = Rs1 + imm; // LW
    break;

  case 16:
    Rz = Rs1 + imm; // JALR
    break;

  case 17:
    Rz = Rs1 + imm; // SB
    Rm = Rs2;
    break;

  case 18:
    Rz = Rs1 + imm; // SH
    Rm = Rs2;
    break;

  case 19:
    Rz = Rs1 + imm; // SW
    Rm = Rs2;
    break;

  case 20:

    if (Rs1 == Rs2)
    { // BEQ
      Rz = 1;
    }
    else
    {
      Rz = 0;
    }
    break;

  case 21:
    if (Rs1 != Rs2)
    { // BNE
      Rz = 1;
    }
    else
    {
      Rz = 0;
    }
    break;

  case 22:
    if (Rs1 < Rs2)
    { // BLT
      Rz = 1;
    }
    else
    {
      Rz = 0;
    }
    break;

  case 23:
    if (Rs1 >= Rs2)
    { // BGE
      Rz = 1;
    }
    else
    {
      Rz = 0;
    }
    break;

  case 24:
    Rz = imm; // LUI
    break;

  case 25:
    Rz = PC + imm - 4; // AUIPC
    break;

  case 26:
    // JAL
    break;

  default:
    break;
  }
}




// perform the memory operation
void mem()
{
  if (control == 13)
  {
    Ry = MEM[Rz];
    int temp = 0x80;
    temp = temp & Ry;
    if (Ry == 0x80)
    {
      temp = 0xffffff00;
      Ry |= temp;
    }
    else
    {
      temp = 0xff;
      Ry &= temp;
    }
  }
  else if (control == 14)
  {
    Ry = read_word(MEM, Rz);
    int temp = 0x8000;
    temp = temp & Ry;
    if (Ry == 0x8000)
    {
      temp = 0xffff0000;
      Ry |= temp;
    }
    else
    {
      temp = 0xffff;
      Ry &= temp;
    }
  }
  else if (control == 15)
  {
    Ry = read_word(MEM, Rz);
  }
  else if (control == 16)
  {
    temp_PC = PC;
    PC = Rz;
  }
  else if (control == 17)
  {
    MEM[Rz] = Rm;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "Result: MEM at 0x%x = 0x%x\n", Rz, Rm);
    fclose(filePointer);
  }
  else if (control == 18)
  {
    MEM[Rz] = Rm % 256;
    int temp = Rm >> 8;
    MEM[Rz + 1] = temp % 256;
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "Result: MEM at 0x%x = 0x%x\n", Rz, Rm);
    fclose(filePointer);
  }
  else if (control == 19)
  {
    write_word(MEM, Rz, Rm);
    filePointer = fopen("INS_OUT.mem", "a");
    fprintf(filePointer, "Result: MEM at 0x%x = 0x%x\n", Rz, Rm);
    fclose(filePointer);
  }
  else if (control == 20 || control == 21 || control == 22 || control == 23)
  {
    if (Rz == 1)
    {
      PC -= 4;

      PC += imm;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "Result: PC=0x%x , PC=0x%x\n", PC);
      fclose(filePointer);
    }
    else
    {
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "Result: No change\n");
      fclose(filePointer);
    }
  }
  else if (control == 26)
  {

    temp_PC = PC;

    PC -= 4;
    PC += imm;
  }
  else
  {
    Ry = Rz;
  }
  X[0] = 0;
}




// writes the results back to register file
void write_back()
{
  if (control == 17 || control == 18 || control == 19 || control == 20 || control == 21 || control == 22 || control == 23)
  {
    return;
  }
  else if (control == 26)
  {

    // X[Rd] = temp_PC;
    if (Rd != 0)
    {
      X[Rd] = temp_PC;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "Result: X%d=%d , PC=0x%x\n", Rd, temp_PC, PC);
      fclose(filePointer);
    }
    else
    {
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "Result: X%d=0 , PC=0x%x\n", Rd, PC);
      fclose(filePointer);
    }
  }
  else if (control == 16)
  {

    if (Rd != 0)
    {
      X[Rd] = temp_PC;
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "Result: X%d=%d , PC=0x%x\n", Rd, temp_PC, PC);
      fclose(filePointer);
    }
    else
    {
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "Result: X%d=0 , PC=0x%x\n", Rd, PC);
      fclose(filePointer);
    }
  }
  else
  {

    X[Rd] = Ry;
    if (Rd != 0)
    {
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "Result: X%d=%d\n", Rd, Ry);
      fclose(filePointer);
    }
    else
    {
      filePointer = fopen("INS_OUT.mem", "a");
      fprintf(filePointer, "Result: X%d=0\n", Rd);
      fclose(filePointer);
    }
  }
  X[0] = 0;
}

void run_riscvsim()
{
  clock_time = clock();
  filePointer = fopen("INS_OUT.mem", "w");
  fprintf(filePointer, "=====START=====\n");
  fclose(filePointer);
  while (1)
  {
    // char ch;
    // cout<<"Press Enter to run the step!!";
    // scanf("%c",&ch);


    fetch();
    decode();
    execute();
    mem();
    write_back();
    cycle++;
  }
}