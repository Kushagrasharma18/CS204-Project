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
static unsigned int X[32];
// flags
// memory
static int MEM[4000];
uint32_t IR;
uint32_t PC = 0x0;
// intermediate datapath and control path signals
static unsigned int instruction_word;
static unsigned int operand1;
static unsigned int operand2;
uint32_t opcode;
uint32_t funct3;
uint32_t funct7;
int32_t imm_i;
int32_t imms;
int32_t immb;
int32_t imm_u;
int32_t immj;
void run_riscvsim()
{
  while (1)
  {
    fetch();
    decode();
    execute();
    mem();
    write_back();
  }
}

// it is used to set the reset values
// reset all registers and memory content to 0
void reset_proc()
{
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
    write_word(MEM, address, instruction);
  }
  fclose(fp);
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
  fclose(fp);
}

// should be called when instruction is swi_exit
void swi_exit()
{
  write_data_memory();
  exit(0);
}

// reads from the instruction memory and updates the instruction register
void fetch()
{
  IR = *(MEM + PC);

  // Increment the program counter
  PC += 4;
}
// reads the instruction register, reads operand1, operand2 fromo register file, decides the operation to be performed in execute stage
void decode()
{
  opcode = IR & 0x7F;        // Extract opcode
  funct3 = (IR >> 12) & 0x7; // Extract funct3
  funct7 = IR >> 25;         // Extract funct7
  imm_i = (int32_t)IR >> 20; // Extract immediate for I format
  // uint32_t imm_s = ((int32_t)IR >> 20) & 0xFFF; // Extract immediate for S format

  // Assume that "instruction" variable contains the S-type instruction
  imms = ((IR >> 7) & 0x1F); // Extract bits 11-5
  imms |= (IR >> 25) << 5;   // Extract bits 31-25 and shift left by 5

  // uint32_t imm_b = ((int32_t)IR >> 20) & 0xFFF; // Extract immediate for B format
  immb = 0;
  immb |= ((IR >> 31) ) << 12; // imm[12]
  immb |= ((IR >> 7) & 0x1) << 11;  // imm[11]
  immb |= ((IR >> 25) & 0x3f) << 5; // imm[10:5]
  immb |= ((IR >> 8) & 0xf) << 1;   // imm[4:1]

  imm_u = IR & 0xFFFFF000; // Extract immediate for U format

  // immj = 0;
  // immj |= ((IR >> 31) & 0x1) << 20;  // imm[20]
  // immj |= ((IR >> 12) & 0xff) << 12; // imm[19:12]
  // immj |= ((IR >> 20) & 0x1) << 11;  // imm[11]
  // immj |= ((IR >> 21) & 0x1f) << 1;  // imm[10:1]
   immj = 0;
  immj |= ((IR >> 31) ) << 20;  // imm[20]
  immj |= ((IR >> 12) & 0xff) << 12; // imm[19:12]
  immj |= ((IR >> 20) & 0x1) << 11;  // imm[11]
  immj |= ((IR >> 21) & 0x3ff) << 1;  // imm[10:1]
}
// executes the ALU operation based on ALUop
void execute()
{
  switch (opcode)
  {
  case 0x33:
    switch (funct3)
    {
    case 0x0:
      switch (funct7)
      {
      case 0x0: // ADD
        break;

      case 0x2: // SUB
        break;

      default:
        cout << "Wrong function 7 value" << endl;
        break;
      }
      break;

    case 0x1: // sll
      break;

    case 0x2: // slt
      break;

    case 0x4: // xor
      break;

    case 0x5:
      switch (funct7)
      {
      case 0x0: // srl
        break;

      case 0x2: // sra
        break;

      default:
        cout << "Wrong function 7 value" << endl;
        break;
      }
      break;

    case 0x6: // or
      break;

    case 0x7: // AND
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      break;
    }
    break;

  case 0x13:
    switch (funct3)
    {
    case 0x0: // addi
      break;

    case 0x6: // ori
      break;

    case 0x7: // andi
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      break;
    }
    break;

  case 0x03:
    switch (funct3)
    {
    case 0x0: // lb
      break;

    case 0x1: // lh
      break;

    case 0x2: // lw
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      break;
    }

    break;

  case 0x23:
    switch (funct3)
    {
    case 0x0: // sb
      break;

    case 0x1: // sh
      break;

    case 0x2: // sw
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      break;
    }
    break;

  case 0x63:
    switch (funct3)
    {
    case 0x0: // beq
      break;

    case 0x1: // bne
      break;

    case 0x4: // blt
      break;

    case 0x5: // bge
      break;

    default:
      cout << "Wrong function 3 value" << endl;
      break;
    }
    break;
  
  case 0x6f://jal
    break;

  case 0x37://lui
    break;

  case 0x17://auipc
    break;
  
  case 0x67://jalr
    break;

  }
}
// perform the memory operation
void mem()
{
}
// writes the results back to register file
void write_back()
{
}

int read_word(char *mem, unsigned int address)
{
  int *data;
  data = (int *)(mem + address);
  return *data;
}

void write_word(char *mem, unsigned int address, unsigned int data)
{
  int *data_p;
  data_p = (int *)(mem + address);
  *data_p = data;
}
