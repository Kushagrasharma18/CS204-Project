#include <bits/stdc++.h>
#include <iostream>
#include "myRISCVsim.h"
#include <stdlib.h>
// #include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
using namespace std;

int main()
{
  reset_proc();
  load_program_memory();
  run_riscvsim();
}