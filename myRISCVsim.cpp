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
#include "myRISCVSim.h"
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
static unsigned int instruction_word;
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
static int clock1 = 0;
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




// it is used to set the reset values
// reset all registers and memory content to 0
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





// writes the data memory in "data_out.mem" file
void write_data_memory()
{
  FILE *fp;
  unsigned int i;
  fp = fopen("data_out.mem", "w");
  if (fp == NULL)
  {
    printf("Error opening dataout.mem file for writing\n");
    return;
  }

  for (i = 0; i < 4000; i = i + 4)
  {
    fprintf(fp, "%x %x\n", i, read_word(MEM, i));
  }
  for (i = 0; i < 32; i++)
  {
    fprintf(fp, "%d %x (%d)\n", i, X[i], X[i]);
  }
  fclose(fp);
}


// should be called when instruction is swi_exit
void swi_exit()
{
  write_data_memory();
  cout<<"cycles:"<<cycle<<"*"<<endl;
  exit(0);
}


// reads from the instruction memory and updates the instruction register
void fetch()
{
  IR = read_word(MEM, PC);

  // Increment the program counter
  PC += 4;
}


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
  
  temp |= (i >> 25) << 5;
  return temp;
}


int imm_s(int i)
{
  int temp = 0x00000000;
  temp = ((i >> 7) & 0x1F);
  temp |= (i >> 25) << 5;
  return temp;
}


int imm_b(int i)
{
  int temp = 0;
  temp |= ((i >> 31)) << 12;       // imm[12]
  temp |= ((i >> 7) & 0x1) << 11;  // imm[11]
  temp |= ((i >> 25) & 0x3f) << 5; // imm[10:5]
  temp |= ((i >> 8) & 0xf) << 1;   // imm[4:1]
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
  temp |= ((i >> 31)) << 20;        // imm[20]
  temp |= ((i >> 12) & 0xff) << 12; // imm[19:12]
  temp |= ((i >> 20) & 0x1) << 11;  // imm[11]
  temp |= ((i >> 21) & 0x3ff) << 1; // imm[10:1]
  return temp;
}


int func_7(int i)
{
  int temp = 0;
  temp = (i >> 25) << 5;
  return temp;
}


int func_3(int i)
{
  int temp = 0;
  temp = (i >> 25) & 0x7;
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
  switch (funct3)
  {
  case 0:
    switch (funct7)
    {
    case 0:                                             // ADD
      control = 1;
      break;

    case 32:                                            // SUB
      control = 2;
      break;

    default:
      cout << "Wrong function 7 value" << endl;

      break;
    }
    break;

  case 1:                                               // sll
    control = 3;
    break;

  case 2:                                               // slt
    control = 4;
    break;

  case 4:                                               // xor
    control = 5;
    break;

  case 5:

    switch (funct7)
    {
    case 0:                                             // srl
      control = 6;
      break;

    case 32:                                            // sra
      control = 7;
      break;

    default:
      cout << "Wrong function 7 value" << endl;
      break;
    }
    break;

  case 6:                                               // or
    control = 8;
    break;

  case 7:                                               // AND
    control = 9;
    break;

  default:
    cout << "Wrong function 3 value" << endl;
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
    case 0:                                             // addi
      control = 10;
      break;

    case 6:                                             // ori
      control = 11;
      break;

    case 7:                                             // andi
      control = 12;
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      break;
    }
  }
  else if (opc == 3)
  {
    switch (funct3)
    {
    case 0:                                             // lb
      control = 13;
      break;

    case 1:                                             // lh
      control = 14;
      break;

    case 2:                                             // lw
      control = 15;
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      break;
    }
  }
  else
  {
    control = 16;                                       // jalr
  }
}


void s_type(int i)
{
  imm = imm_s(i);
  Rs2 = r_s_2(i);
  Rs1 = r_s_1(i);
  int funct3 = func_3(i);
  switch (funct3)
  {
  case 0x0:                                             // sb
    control = 17;
    break;

  case 0x1:                                             // sh
    control = 18;
    break;

  case 0x2:                                             // sw
    control = 19;
    break;

  default:
    cout << "Wrong function 3 value" << endl;
    break;
  }
}


void b_type(int i)
{
  imm = imm_b(i);
  Rs2 = r_s_2(i);
  Rs1 = r_s_1(i);
  int funct3 = func_3(i);
  switch (funct3)
  {
  case 0x0:                                             // beq
    control = 20;
    break;

  case 0x1:                                             // bne
    control = 21;
    break;

  case 0x4:                                             // blt
    control = 22;
    break;

  case 0x5:                                             // bge
    control = 23;
    break;

  default:
    cout << "Wrong function 3 value" << endl;
    break;
  }
}


void u_type(int i)
{
  imm = imm_u(i);
  Rd = r_d(i);
  int opc = op_code(i);
  if (opc == 55)
  {
    control = 24;                                       // lui
  }
  else
  {
    control = 25;                                       // auipc
  }
}


void j_type(int i)
{
  imm = imm_j(i);
  Rd = r_d(i);
  control = 26;                                       //jal
}


void decode()
{
  opcode = op_code(IR);                               // Extract opcode
  if(opcode==51){
    r_type(IR);
  }
  else if(opcode==19||opcode==3||opcode==103){
    i_type(IR);
  }
  else if(opcode==35){
    s_type(IR);
  }
  else if(opcode==99){
    b_type(IR);
  }
  else if(opcode==55||opcode==23){
    u_type(IR);
  }
  else if(opcode==111){
    j_type(IR);
  }
  else{
    cout<<"Wrong OPcode!!"<<endl;
  }
  
  
}


// executes the ALU operation based on ALUop
void execute()
{
  switch (control)
  {
  case 1:
    Rz=Rs1+Rs2;                           //ADD
    break;

  case 2:
    Rz=Rs1-Rs2;                           //SUB
    break;

  case 3:
    Rz=Rs1<<Rs2;                          //SLL
    break;

  case 4:
    Rz=(Rs1<Rs2)?1:0;                     //SLT
    break;

  case 5:
    Rz=Rs1^Rs2;                           //XOR
    break;

  case 6:
    Rz=(int)((unsigned int)Rs1>>Rs2);     //SRL
    break;

  case 7: 
    Rz=Rs1>>Rs2;                          //SRA
    break;

  case 8:
    Rz=Rs1|Rs2;                           //OR
    break;

  case 9:
    Rz=Rs1&Rs2;                           //AND
    break;

  case 10:
    Rz=Rs1+imm;                           //ADDI
    break;

  case 11:
    Rz=Rs1|imm;                           //ORI
    break;

  case 12:
    Rz=Rs1&imm;                           //ANDI
    break;

  case 13:
    Rz=Rs1+imm;                           //LB
    break;

  case 14:
    Rz=Rs1+imm;                           //LH
    break;

  case 15:
    Rz=Rs1+imm;                           //LW
    break;

  case 16:
    Rz=Rs1+imm;                           //JALR
    break;

  case 17:
    Rz=Rs1+imm;                           //SB
    Rm=Rs2;
    break;

  case 18:
    Rz=Rs1+imm;                           //SH
    Rm=Rs2;
    break;

  case 19:
    Rz=Rs1+imm;                           //SW
    Rm=Rs2;
    break;

  case 20:
    if(Rs1==Rs2){                         //BEQ
      Rz=1;
    }
    else{
      Rz=0;
    }
    break;

  case 21:
    if(Rs1!=Rs2){                         //BNE
      Rz=1;
    }
    else{
      Rz=0;
    }
    break;

  case 22:
    if(Rs1<Rs2){                          //BLT
      Rz=1;
    }
    else{
      Rz=0;
    }
    break;

  case 23:
    if(Rs1>=Rs2){                         //BGE
      Rz=1;
    }
    else{
      Rz=0;
    }
    break;

  case 24:
    Rz=imm<<12;                           //LUI
    break;

  case 25:
    Rz=imm;                               //AUIPC
    break;

  case 26:
                                          //JAL
    break;

  default:
    break;
  }
}


// perform the memory operation
void mem()
{
  if(control==13){
    Ry=MEM[Rz];
    int temp=0x80;
    temp=temp&Ry;
    if(Ry==0x80){
      temp=0xffffff00;
      Ry|=temp;
    }
    else{
      temp=0xff;
      Ry&=temp;
    }
  }
  else if(control==14){
    Ry=read_word(MEM,Rz);
    int temp=0x8000;
    temp=temp&Ry;
    if(Ry==0x8000){
      temp=0xffff0000;
      Ry|=temp;
    }
    else{
      temp=0xffff;
      Ry&=temp;
    }
    
  }
  else if(control==15){
    Ry=read_word(MEM,Rz);
  }
  else if(control==16){
    temp_PC=PC;
    PC=Rz;
  }
  else if(control==17){
    MEM[Rz]=Rm;
  }
  else if(control==18){
    MEM[Rz]=Rm%256;
    int temp=Rm>>8;
    MEM[Rz+1]=Rm%256;
  }
  else if(control==19){
    write_word(MEM,Rz,Rm);
  }
  else if(control==20||control==21||control==22||control==23){
    if(Rz==1){
      PC-=4;
      PC+=imm;
    }
  }
  else if(control==26){
    temp_PC=PC;
    PC-=4;
    PC+=imm;
  }
  else{
    Ry=Rz;
  }

}


// writes the results back to register file
void write_back()
{
  if(control==17||control==18||control==19||control==20||control==21||control==22||control==23){
    return;
  }
  else if(control==16||control==26){
    X[Rd]==temp_PC;
  }
  else{
    X[Rd]=Ry;
  }
}



// load_program_memory reads the input memory, and pupulates the instruction
//  memory
void load_program_memory(char *file_name)
{
  FILE *fp;
  unsigned int address, instruction;
  fp = fopen("input.mc", "r");
  if (fp == NULL)
  {
    printf("Error opening input mem file\n");
    exit(1);
  }
  while (fscanf(fp, "%x %x", &address, &instruction) != EOF)
  {
    if (instruction == 0xffffffff)
      continue;
    write_word(MEM, address, instruction);
  }
  fclose(fp);
  for (int i = 0; i < 32; i++)
  {
    X[i] = 0x00000000;
  }
  X[2] = stackPointer;
}



void run_riscvsim()
{
  while (1)
  {
    fetch();
    decode();
    execute();
    mem();
    write_back();
    cycle++;
  }
}