import sys

x = []  # Registers
x.append(0)
for i in range(1, 32):
    x.append(0)
    if (i == 3):
        x[i] = int("0x10000000", 16)  # gp
    elif (i == 2):
        x[i] = int("0x7FFFFFF0", 16)  # sp

memory = {}


class five_steps:
    def __init__(self):
        self.buf = []
        self.buffer = []
        self.PC = 0x0
        self.PC_temp = self.PC
        self.clock = 0
        self.cycle = 0
        self.IF = ''
        
        ############ DECODE   ###########
        self.operation = ''
        self.rs1 = ''
        self.rs2 = ''
        self.rd = ''
        self.rd_array1 = []
        self.rd_array2 = []
        self.imm = ''
        self.jot = 0
        ####### END     #########
        
        ############ MEMORY   ###########
        self.string = ''
        self.dataa = ''
        self.address = -1

        self.operation1 = ''
        self.dataa1 = ''
        self.rd1 = ''
        self.imm1 = ''
        self.address1 = -1
        ####### END     #########
        
        self.rd2 = ''
        self.jot2 = 0
        self.total_cycles = 0
        self.rs1_a = 0
        self.rs2_b = 0
        self.rs1_bool = False
        self.rs2_bool = False

        self.stalling1 = False

        #####  Previous called memory   #####
        self.previous_memory_operation = ''
        self.previous_memory_dataa = ''
        self.previous_memory_rd = ''
        self.previous_memory_imm = ''
        self.previous_memory_address = -1

        #####  Previous called writeback   #####
        self.previous_writeback_rd = ''
        self.previous_writeback_content = 0

        self.PC_changed_in_sb_format = self.PC
        self.PC_jumped_count = self.PC
        self.check_sb_format_execution = False

        self.ind = 0

        #####  stats to be printed at the end of simulation  #####
        self.ninstructions = 0  # total no.of instructions executed
        self.cpi = 0
        self.DT_instructions = 0
        self.ALU_instructions = 0
        self.control_instructions = 0
        self.stalls = 0
        self.data_hazards = 0
        self.control_hazards = 0
        self.mispredictions = 0
        self.DH_stalls = 0  # stalls due to data hazards
        self.CH_stalls = 0  # stalls due to control hazards

    def fetch(self, binaryCode):
        self.IF = binaryCode
        self.PC_temp = self.PC
        
        print(
            "FETCH:Fetch instruction " + hex(int(self.IF, 2))[2:].zfill(8) + " from address " + hex(self.PC)[2:].zfill(
                8))
        if (knob1 == 1):
            self.buffer.append([])
            self.buffer[self.ind].append({"Fetch-Decode buffer": "", "binaryCode": self.IF, "PC": self.PC})
            
        self.PC += 4
        

    def decode(self, binaryInstruction):
        if (len(binaryInstruction) == 0):
            print("Returning")
            return

        opcode = binaryInstruction[25:32]

        R_oper = ["0110011"]
        I_oper = ["0010011", "0000011", "1100111"]
        S_oper = ["0100011"]
        SB_oper = ["1100011"]
        U_oper = ["0110111", "0010111"]
        UJ_oper = ["1101111"]

        if opcode in R_oper:
            # decode

            funct7 = binaryInstruction[0:7]
            rs2 = binaryInstruction[7:12]
            rs1 = binaryInstruction[12:17]
            funct3 = binaryInstruction[17:20]
            rd = binaryInstruction[20:25]
            opcode = binaryInstruction[25:32]
            self.rs1 = rs1
            self.rs2 = rs2
            self.rd = rd
            self.imm = ''

            if (opcode == "0110011"):
                if (funct7 == "0000000"):
                    if (funct3 == "000"):
                        self.operation = "add"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:", int(self.rs2, 2), ",destination register:", int(self.rd, 2),
                              end=" \n", sep=" ")
                        


                    elif (funct3 == "111"):

                        self.operation = "and"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    elif (funct3 == "110"):

                        self.operation = "or"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    elif (funct3 == "001"):

                        self.operation = "sll"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        


                    elif (funct3 == "010"):

                        self.operation = "slt"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    elif (funct3 == "101"):

                        self.operation = "srl"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    elif (funct3 == "100"):

                        self.operation = "xor"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    else:
                        print("Error")
                elif (funct7 == "0100000"):
                    if (funct3 == "000"):

                        self.operation = "sub"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        
                    elif (funct3 == "101"):

                        self.operation = "sra"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    else:
                        print("Error")
                elif (funct7 == "0000001"):
                    if (funct3 == "000"):

                        self.operation = "mul"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    elif (funct3 == "100"):
                        self.operation = "div"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    elif (funct3 == "110"):
                        self.operation = "rem"
                        print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                              ",source register 2:",
                              int(self.rs2, 2),
                              ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                        

                    else:
                        print("Error")
                else:
                    print("Error")
            else:
                print("Error")
        elif opcode in I_oper:
            imm = binaryInstruction[0:12]
            rs1 = binaryInstruction[12:17]
            funct3 = binaryInstruction[17:20]
            rd = binaryInstruction[20:25]
            opcode = binaryInstruction[25:32]

            self.rs1 = rs1
            self.rs2 = ''
            self.rd = rd
            self.imm = imm

            
            
            if (opcode == "0000011"):
                if (funct3 == "000"):
                    # lb

                    self.operation = "lb"
                    print("Decode -> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                          ",Immediate:", imm,
                          ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                   
                elif (funct3 == "001"):

                    self.operation = "lh"
                    print("Decode -> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                          ",Immediate:", imm,
                          ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                    # lh

                    
                elif (funct3 == "010"):

                    self.operation = "lw"
                    print("Decode -> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                          ",Immediate:", imm,
                          ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                    # lw

                    
                else:
                    print("Error")
                    
            elif (opcode == "0010011"):
                if (funct3 == "000"):

                    self.operation = "addi"
                    print("Decode -> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                          ",Immediate:", imm,
                          ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                    # addi
                    
                elif (funct3 == "111"):

                    self.operation = "andi"
                    print("Decode -> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                          ",Immediate:", imm,
                          ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                    # andi
                    
                elif (funct3 == "110"):
                    # ori
                    self.operation = "ori"
                    print("Decode -> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                          ",Immediate:", imm,
                          ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                    

                else:
                    print("Error")
            elif (opcode == "1100111"):
                if (funct3 == "000"):

                    self.operation = "jalr"
                    print("Decode -> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                          ",Immediate:", imm,
                          ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                    # jalr
                    

                else:
                    print("Error")
        elif opcode in S_oper:

            func3 = binaryInstruction[17:20]  # funct3
            rs1 = binaryInstruction[12:17]  # source register1
            rs2 = binaryInstruction[7:12]  # source register2
            imm = binaryInstruction[0:7] + binaryInstruction[20:25]  # offset added to base adress

            self.rs1 = rs1
            self.rs2 = rs2
            self.rd = ""
            self.imm = imm

            Sr1 = 0  # for decimal value of source register1
            Sr2 = 0  # for decimal value of source register2
            for i in range(0, 5):
                if (rs1[i] == '1'):
                    Sr1 = Sr1 + pow(2, 4 - i)
                if (rs2[i] == '1'):
                    Sr2 = Sr2 + pow(2, 4 - i)

            Offset = 0
            for i in range(0, 12):
                if (imm[i] == '1'):
                    Offset = Offset + pow(2, 11 - i)

            if (func3 == '000'):

                self.operation = "sb"
                print("Decode-> operation: ", self.operation, ",source register 1:", int(self.rs1, 2),
                      ",Source register 2:",
                      int(self.rs2, 2),
                      ",Immediate: ", imm, end=" \n", sep=" ")
                

                

            elif (func3 == '001'):

                self.operation = "sh"
                print("Decode-> operation: ", self.operation, ",source register 1:", int(self.rs1, 2),
                      ",Source register 2:",
                      int(self.rs2, 2),
                      ",Immediate: ", imm, end=" \n", sep=" ")
                

            elif (func3 == '010'):

                self.operation = "sw"
                print("Decode-> operation: ", self.operation, ",source register 1:", int(self.rs1, 2),
                      ",Source register 2:",
                      int(self.rs2, 2),
                      ",Immediate: ", imm, end=" \n", sep=" ")
                
            else:
                print("ERROR")
        elif opcode in SB_oper:
            funct3 = binaryInstruction[17:20]
            rs1 = binaryInstruction[12:17]
            rs2 = binaryInstruction[7:12]
            imm = binaryInstruction[0] + binaryInstruction[24] + binaryInstruction[1:7] + binaryInstruction[20:24]

            self.rs1 = rs1
            self.rs2 = rs2
            self.rd = ''
            self.imm = imm

            if funct3 == '000':

                self.operation = "beq"
                print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                      ",Source register 2:",
                      int(self.rs2, 2),
                      ",Immediate: ", imm, end=" \n", sep=" ")
                
            elif funct3 == '001':

                self.operation = "bne"
                print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                      ",Source register 2:",
                      int(self.rs2, 2),
                      ",Immediate: ", imm, end=" \n", sep=" ")
                
            elif funct3 == '101':

                self.operation = "bge"
                print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                      ",Source register 2:",
                      int(self.rs2, 2),
                      ",Immediate: ", imm, end=" \n", sep=" ")
                
            elif funct3 == '100':

                self.operation = "blt"
                print("Decode-> operation :", self.operation, ",source register 1:", int(self.rs1, 2),
                      ",Source register 2:",
                      int(self.rs2, 2),
                      ",Immediate: ", imm, end=" \n", sep=" ")
                
            else:
                print("Error")
        elif opcode in U_oper:
            # decode

            imm = binaryInstruction[0:20]
            rd = binaryInstruction[20:25]
            opcode = binaryInstruction[25:32]  # opcode is enough to distinguish u and uj format instructions

            self.rs1 = ''
            self.rs2 = ''
            self.rd = rd
            self.imm = imm

            if (opcode == "0010111"):
                # auipc
                self.operation = "auipc"
                print("Decode -> operation :", self.operation, ",Immediate:", imm,
                      ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                

            elif (opcode == "0110111"):
                # lui

                self.operation = "lui"
                print("Decode -> operation :", self.operation, ",Immediate:", imm,
                      ",destination register : ", int(self.rd, 2), end=" \n", sep=" ")
                
            else:
                print("Error")
        elif opcode in UJ_oper:
            opcode = binaryInstruction[25:32]
            imm = binaryInstruction[0] + binaryInstruction[12:20] + binaryInstruction[11] + binaryInstruction[1:11]
            rd = binaryInstruction[20:25]

            self.rs1 = ''
            self.rs2 = ''
            self.rd = rd
            self.imm = imm

            if (opcode == "1101111"):
                # jal

                self.operation = "jal"
                print("Decode:-> operation: ", self.operation, ",destinaton register:", int(self.rd, 2), ",Immediate: ",
                      imm, end=" \n", sep=" ")

            else:
                print("Error")
        else:
            print("Error")
        if (knob1 == 1):
            self.buffer.append([])
            self.buffer[self.ind].append({"Decode-Execute buffer": "", "rs1": self.rs1, "rs2": self.rs2, "rd": self.rd, "imm": self.imm,"operation": self.operation})
            

    def execute(self):
        
        
        if (self.operation == "add" or self.operation == "and" or self.operation == "or" or self.operation == "sll"):

            self.execute_add_and_or_sll(self.operation, self.rs1, self.rs2, self.rd)
        elif (self.operation == "xor" or self.operation == "mul" or self.operation == "div" or self.operation == "rem"):

            self.execute_xor_mul_div_rem(self.operation, self.rs1, self.rs2, self.rd)


        elif (self.operation == "slt" or self.operation == "srl" or self.operation == "sub" or self.operation == "sra"):

            self.execute_slt_srl_sub_sra(self.operation, self.rs1, self.rs2, self.rd)

        elif (self.operation == "addi" or self.operation == "andi" or self.operation == "ori"):
            temp = self.imm
            if (temp[0:1] == '1'):
                check = str(temp)
                check = check[::-1]
                temp = self.findnegative(check)
            else:
                temp = int(temp, 2)
            self.execute_addi_andi_ori(self.operation, self.rd, self.rs1, self.imm)


        elif (self.operation == "lui" or self.operation == "auipc"):

            temp = self.imm
            if (temp[0:1] == '1'):
                check = str(temp)
                check = check[::-1]
                temp = self.findnegative(check)
            else:
                temp = int(temp, 2)
            self.execute_lui_auipc(self.operation, self.rd, self.imm, self.PC_temp)

        elif (self.operation == "bge" or self.operation == "blt"):

            temp = self.imm
            if (temp[0:1] == '1'):
                check = str(temp)
                check = check[::-1]
                temp = self.findnegative(check)
            else:
                temp = int(temp, 2)
            self.execute_bge_blt(self.operation, self.rs1, self.rs2, self.imm, self.PC_temp)

        elif (self.operation == "beq" or self.operation == "bne"):

            temp = self.imm
            if (temp[0:1] == '1'):
                check = str(temp)
                check = check[::-1]
                temp = self.findnegative(check)
            else:
                temp = int(temp, 2)
            self.execute_beq_bne(self.operation, self.rs1, self.rs2, self.imm, self.PC_temp)


        elif (self.operation == "jal"):

            temp = self.imm
            if (temp[0:1] == '1'):
                check = str(temp)
                check = check[::-1]
                temp = self.findnegative(check)
            else:
                temp = int(temp, 2)
            self.execute_jal(self.operation, self.rd, self.imm, self.PC_temp)

        elif (self.operation == "jalr"):

            temp = self.imm
            if (temp[0:1] == '1'):
                check = str(temp)
                check = check[::-1]
                temp = self.findnegative(check)
            else:
                temp = int(temp, 2)
            self.execute_jalr(self.operation, self.rs1, self.rd, self.imm, self.PC_temp)
        elif (self.operation == "sw" or self.operation == "sh" or self.operation == "sb"):

            temp = self.imm
            if (temp[0:1] == '1'):
                check = str(temp)
                check = check[::-1]
                temp = self.findnegative(check)
            else:
                temp = int(temp, 2)
            # print("executed store\n")
            self.executeStore(self.operation, self.rs1, self.rs2, self.imm)
        elif (self.operation == "lw" or self.operation == "lh" or self.operation == "lb"):

            temp = self.imm
            if (temp[0:1] == '1'):
                check = str(temp)
                check = check[::-1]
                temp = self.findnegative(check)
            else:
                temp = int(temp, 2)
            self.executeRead(self.operation, self.rs1, self.rd, self.imm)
            
        self.operation1 = self.operation
        self.dataa1 = self.dataa
        self.rd1 = self.rd
        self.imm1 = self.imm
        self.address1 = self.address

        if (knob1 == 1):
            self.buffer.append([])
            self.buffer[self.ind].append({"Execute-memory buffer": "", "operation": self.operation, "memoryData": self.dataa, "rd": self.rd, "imm": self.imm,"address": self.address, "executionAnswer": self.jot})
            

    def execute_add_and_or_sll(self, string, rs1, rs2, rd):
        if (string == "add"):  # executing add
            rs1 = int(rs1, 2)
            rs2 = int(rs2, 2)
            rd = int(rd, 2)

            if (self.rs1_bool == False):
                self.rs1_a = x[rs1]
            if (self.rs2_bool == False):
                self.rs2_b = x[rs2]

            s = self.rs1_a + self.rs2_b

            print("Execute :", string, self.rs1_a, "and", self.rs2_b)
            
            if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                self.jot = s


        elif (string == "and"):  # executing and
            rs1 = int(rs1, 2)
            rs2 = int(rs2, 2)
            rd = int(rd, 2)

            if (self.rs1_bool == False):
                self.rs1_a = x[rs1]
            if (self.rs2_bool == False):
                self.rs2_b = x[rs2]

            s = self.rs1_a & self.rs2_b

            print("Execute :", string, self.rs1_a, "and", self.rs2_b)
            
            if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                self.jot = s


        elif (string == "or"):  # executing or
            rs1 = int(rs1, 2)
            rs2 = int(rs2, 2)
            rd = int(rd, 2)

            if (self.rs1_bool == False):
                self.rs1_a = x[rs1]
            if (self.rs2_bool == False):
                self.rs2_b = x[rs2]

            s = self.rs1_a | self.rs2_b

            print("Execute :", string, self.rs1_a, "and", self.rs2_b)

            
            if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                self.jot = s


        elif (string == "sll"):  # executing sll
            rs1 = int(rs1, 2)
            rs2 = int(rs2, 2)
            rd = int(rd, 2)

            if (self.rs1_bool == False):
                self.rs1_a = x[rs1]
            if (self.rs2_bool == False):
                self.rs2_b = x[rs2]

            s = self.rs1_a << self.rs2_b
            print("Execute :", string, self.rs1_a, "and", self.rs2_b)
            
            if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                self.jot = s

    def execute_xor_mul_div_rem(self, string, rs1, rs2, rd):
        rd = int(rd, 2)
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)

        if (self.rs1_bool == False):
            self.rs1_a = x[rs1]
        if (self.rs2_bool == False):
            self.rs2_b = x[rs2]

        if string == 'xor':
            output = self.rs1_a ^ self.rs2_b
            if -(pow(2, 31)) <= output <= (pow(2, 31)) - 1:  # Underflow and overflow
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                
                self.jot = output
                
        elif string == 'mul':
            output = self.rs1_a * self.rs2_b
            if -(pow(2, 31)) <= output <= (pow(2, 31)) - 1:  # Underflow and overflow
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                
                self.jot = output
                
        elif string == "div":
            output = self.rs1_a // self.rs2_b
            if -(pow(2, 31)) <= output <= (pow(2, 31)) - 1:  # Underflow and overflow
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                
                self.jot = output
                
        elif string == "rem":
            output = self.rs1_a % self.rs2_b
            if -(pow(2, 31)) <= output <= (pow(2, 31)) - 1:  # Underflow and overflow
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                
                self.jot = output
                

    def execute_lui_auipc(self, string, rd, imm, PC):
        if (imm[0:1] == '1'):
            check = str(imm)
            check = check[::-1]
            imm = self.findnegative(check)
        else:
            imm = int(imm, 2)
        rd = int(rd, 2)

        if string == "lui":  # executing lui
            if (imm <= pow(2, 19) - 1 and imm >= -pow(2, 19)):  # checking range of imm
                temp = 0 | imm
                temp = temp << 12
                if (temp >= -(pow(2, 31)) and temp <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                    print("Execute :", string, x[rd], "and", imm)
                    self.jot = temp
                    
        elif string == "auipc":  # executing auipc
            if (imm <= pow(2, 19) - 1 and imm >= -pow(2, 19)):  # checking range of imm
                temp = 0 | imm
                temp = temp << 12
                temp = temp + PC
                if (temp >= -(pow(2, 31)) and temp <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                    print("Execute :", string, x[rd], "and", imm)
                    self.jot = temp
                    
        else:
            print("Error")

    def execute_slt_srl_sub_sra(self, string, rs1, rs2, rd):
        # slt,sra,srl,sub
        rd = int(rd, 2)
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)

        if (self.rs1_bool == False):
            self.rs1_a = x[rs1]
        if (self.rs2_bool == False):
            self.rs2_b = x[rs2]

        if (string == "slt"):
            if (self.rs1_a < self.rs2_b):
                jot = 1
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                self.jot = jot
                
            else:
                jot = 0
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                self.jot = jot
                
        elif (string == "sra"):
            result = self.rs1_a >> self.rs2_b
            lowerlimit = -1 * (1 << 31)
            upperlimit = (1 << 31) - 1
            if (lowerlimit <= result and result <= upperlimit):  # checking underflow and overflow condition
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                
                self.jot = result
                
        elif (string == "srl"):
            result = self.rs1_a >> self.rs2_b
            lowerlimit = -1 * (1 << 31)
            upperlimit = (1 << 31) - 1
            if (lowerlimit <= result and result <= upperlimit):
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                
                self.jot = result
                
        elif (string == "sub"):
            result = self.rs1_a - self.rs2_b
            lowerlimit = -1 * (1 << 31)
            upperlimit = (1 << 31) - 1
            if (lowerlimit <= result and result <= upperlimit):
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                
                self.jot = result
                

    def execute_addi_andi_ori(self, string, rd, rs1, imm):      #addi,andi,ori
        rs1 = int(rs1, 2)
        rd = int(rd, 2)

        if (self.rs1_bool == False):
            self.rs1_a = x[rs1]

        
        if (imm[0:1] == '1'):
            check = str(imm)
            check = check[::-1]
            imm = self.findnegative(check)
        else:
            imm = int(imm, 2)

        if (string == "addi"):
            if (imm <= pow(2, 11) - 1 and imm >= -pow(2, 11)):  # checking range of imm
                s = self.rs1_a + imm
                if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                    print("Execute :", string, self.rs1_a, "and", imm)
                    

                    self.jot = s
                    

        elif (string == "andi"):
            if (imm <= pow(2, 11) - 1 and imm >= -pow(2, 11)):  # checking range of imm
                s = self.rs1_a & imm
                if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                    print("Execute :", string, self.rs1_a, "and", imm)
                    
                    self.jot = s
                    

        elif (string == "ori"):

            if (imm <= pow(2, 11) - 1 and imm >= -pow(2, 11)):  # checking range of imm
                s = self.rs1_a | imm
                if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                    print("Execute :", string, self.rs1_a, "and", imm)
                    
                    self.jot = s
                   

    def execute_bge_blt(self, string, rs1, rs2, imm, pc):
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        if (imm[0:1] == '1'):
            check = str(imm)
            check = check[::-1]
            imm = self.findnegative(check)
        else:
            imm = int(imm, 2)
        imm = imm << 1

        if (self.rs1_bool == False):
            self.rs1_a = x[rs1]
        if (self.rs2_bool == False):
            self.rs2_b = x[rs2]

        if string == "bge":
            if self.rs1_a >= self.rs2_b:
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                self.check_sb_format_execution = True

                pc = pc + imm
            else:
                print("Execute :No execute")
                
                
                pc = pc + 4
        elif string == 'blt':
            if self.rs1_a < self.rs2_b:
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                self.check_sb_format_execution = True

                pc = pc + imm
            else:
                print("Execute :No execute")

                pc = pc + 4

        self.PC_jumped_count = imm
        self.PC_changed_in_sb_format = pc
        self.PC = pc

    def execute_beq_bne(self, string, rs1, rs2, imm, pc):
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        if (imm[0:1] == '1'):
            check = str(imm)
            check = check[::-1]
            imm = self.findnegative(check)
        else:
            imm = int(imm, 2)
        imm = imm << 1

        if (self.rs1_bool == False):
            self.rs1_a = x[rs1]
        if (self.rs2_bool == False):
            self.rs2_b = x[rs2]

        if (string == 'beq'):
            if (self.rs1_a == self.rs2_b):
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                self.check_sb_format_execution = True
                pc = pc + imm
            else:
                print("Execute :No execute")
                pc = pc + 4
        elif (string == 'bne'):
            if (self.rs1_a != self.rs2_b):
                print("Execute :", string, self.rs1_a, "and", self.rs2_b)
                self.check_sb_format_execution = True
                pc = pc + imm
            else:
                print("Execute :No execute")
                pc = pc + 4

        self.PC_jumped_count = imm
        self.PC_changed_in_sb_format = pc
        self.PC = pc

    def execute_jal(self, string, rd, imm, pc):  #   jal  function
        rd = int(rd, 2)

        if (imm[0:1] == '1'):
            check = str(imm)

            check = check[::-1]
            imm = self.findnegative(check)

        else:
            imm = int(imm, 2)

        imm = imm << 1

        if (string == 'jal'):
            temp = pc
            pc = pc + imm

            jot = temp + 4
            print("Execute :", string, x[rd], "and", imm)
            
            if rd != 0:
                self.jot = jot
                
            
            

        self.PC = pc

    def execute_jalr(self, string, rs1, rd, imm, pc):  #     jalr function
        rs1 = int(rs1, 2)
        rd = int(rd, 2)
        if (imm[0:1] == '1'):
            check = str(imm)
            check = check[::-1]
            imm = self.findnegative(check)
        else:
            imm = int(imm, 2)

        if (self.rs1_bool == False):
            self.rs1_a = x[rs1]

        if (string == 'jalr'):
            temp = pc
            pc = self.rs1_a + imm
            print("Execute :", string, self.rs1_a, "and", imm)
            
            if (rd != 0):
                jot = temp + 4
                self.jot = jot
                
            
            

        self.PC = pc

    def executeStore(self, string, rs1, rs2, imm):
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)

        if (self.rs1_bool == False):
            self.rs1_a = x[rs1]
        if (self.rs2_bool == False):
            self.rs2_b = x[rs2]

        if (imm[0:1] == '1'):
            check = str(imm)
            check = check[::-1]
            imm = self.findnegative(check)
        else:
            imm = int(imm, 2)
        dataa = hex(self.rs2_b)[2:].zfill(8)

        self.dataa = dataa
        if (string == "sw"):
            if (self.rs1_a + imm >= 268435456):  # data segment starts with address 268435456 or 0x10000000
                adds = self.rs1_a + imm  # calculating address
                print("Execute : calculating effective address by adding", self.rs1_a, "and", imm)
                self.string = "sw"
                self.address = adds
        elif (string == "sh"):
            if (self.rs1_a + imm >= 268435456):
                adds = self.rs1_a + imm
                print("Execute : calculating effective address by adding", self.rs1_a, "and", imm)
                self.string = "sh"
                self.address = adds
        elif (string == "sb"):
            if (self.rs1_a + imm >= 268435456):
                adds = self.rs1_a + imm
                print("Execute : calculating effective address by adding", self.rs1_a, "and", imm)
                self.string = "sb"
                self.address = adds

    def MemoryStore(self, string, dataa, address):
        print("Memory: accessed memory location at", address)
        if (string == "sw"):

            memory[address] = dataa[6:]
            memory[address + 1] = dataa[4:6]
            memory[address + 2] = dataa[2:4]
            memory[address + 3] = dataa[0:2]
        elif (string == "sh"):
            memory[address] = dataa[6:]
            memory[address + 1] = dataa[4:6]
        elif (string == "sb"):
            memory[address] = dataa[6:]

    def executeRead(self, string, rs1, rd, imm):
        rs1 = int(rs1, 2)
        rd = int(rd, 2)

        if (self.rs1_bool == False):
            self.rs1_a = x[rs1]

        check = imm
        if (imm[0:1] == '1'):  # imm is a negative number, since sign bit is 1
            check = str(check)
            check = check[::-1]  # reversing the string

            t1 = self.findnegative(check)

            imm = t1
        else:
            imm = int(imm, 2)  # sign bit is 0

        temp1 = self.rs1_a + imm  # calculating address
        self.address = temp1
        print("Execute : calculating effective address by adding", self.rs1_a, "and", imm)
        self.imm = imm
        # self.Memoryread(self, string, temp1, rd, imm)

    def Memoryread(self, string, temp1, rd, imm):  
        # print("imm=",imm)
        if (imm <= pow(2, 11) - 1 and imm >= -pow(2, 11)):  # checking range of imm
            if (string == "lw"):
                if (temp1 >= 268435456):  # data segment starts with address 268435456 or 0x10000000
                    if temp1 in memory:
                        print("Memory: accessed memory location at", temp1)
                        temp2 = memory[temp1 + 3] + memory[temp1 + 2] + memory[temp1 + 1] + memory[temp1]

                        jot = int(temp2, 16)
                        self.jot = jot
                        
                    else:
                        memory[temp1] = "00"
                        memory[temp1 + 1] = "00"
                        memory[temp1 + 2] = "00"
                        memory[temp1 + 3] = "00"
                        self.Memoryread(string, temp1, rd, imm)
                else:
                    print("\n Invalid offset")
                    print(temp1)
            elif string == "lh":
                if temp1 >= 268435456:  # data segment starts with address 268435456 or 0x10000000
                    if temp1 in memory:
                        print("Memory: accessed memory location at", temp1)
                        temp2 = memory[temp1 + 1] + memory[temp1]
                        jot = int(temp2, 16)
                        self.jot = jot
                        
                    else:
                        memory[temp1] = "00"
                        memory[temp1 + 1] = "00"
                        memory[temp1 + 2] = "00"
                        memory[temp1 + 3] = "00"
                        self.Memoryread(string, temp1, rd, imm)
                else:
                    print("\n Invalid offset")
                    print(temp1)
            elif string == "lb":
                if temp1 >= 268435456:  # data segment starts with address 268435456 or 0x10000000
                    if temp1 in memory:
                        print("Memory: accessed memory location at", temp1)
                        temp2 = memory[temp1]
                        jot = int(temp2, 16)
                        self.jot = jot
                        
                    else:
                        memory[temp1] = "00"
                        memory[temp1 + 1] = "00"
                        memory[temp1 + 2] = "00"
                        memory[temp1 + 3] = "00"
                        self.Memoryread(string, temp1, rd, imm)
                else:
                    print("\n Invalid offset")
                    print(temp1)
            else:
                print("\nError")

    def Memory(self, string, dataa, rd, imm, address):
        if (string == "lb" or string == "lw" or string == "lh"):
            self.Memoryread(string, address, rd, imm)
        elif (string == "sb" or string == "sw" or string == "sh"):
            self.MemoryStore(string, dataa, address)
        
        else:
            print("NO memory operation")
        self.rd2 = rd
        self.jot2 = self.jot

        if (knob1 == 1):
            self.buffer.append([])
            self.buffer[self.ind].append({"Memory-WriteBack buffer": "", "rd": self.rd, "writebackAnswer": self.jot})
            

    def WriteBack(self, rd, content):
        if (len(rd) == 0):
            print("WRITEBACK: no writeback ")
            return
        rd = int(rd, 2)
        if rd != 0:
            x[rd] = content
            print("WRITEBACK: write", content, " to x[", rd, "]")
        

    def findnegative(self, string):
        length = len(string)
        neg = -1  # intialize neg with -1
        sum = 0
        i = 0  # counter
        while i <= length - 1:
            if (string[i] == '0'):
                sum += -pow(2, i)
            i = i + 1
        neg = neg + sum
        return neg

    def save_last_called_memory(self):
        self.previous_memory_operation = self.operation1
        self.previous_memory_rd = self.rd1
        self.previous_memory_imm = self.imm1
        self.previous_memory_dataa = self.dataa1
        self.previous_memory_address = self.address1

    def check_already_called_memory(self):
        if (self.previous_memory_operation == self.operation1 and self.previous_memory_rd == self.rd1 and
                self.previous_memory_imm == self.imm1 and self.previous_memory_dataa == self.dataa1 and
                self.previous_memory_address == self.address1):
            return 1
        else:
            return 0

    def save_last_called_writeback(self):
        self.previous_writeback_rd = self.rd2
        self.previous_writeback_content = self.jot2

    def check_already_called_writeback(self):
        if (self.previous_writeback_rd == self.rd2 and self.previous_writeback_content == self.jot2):
            return 1
        else:
            return 0

    def clear_already_called_writeback(self):
        self.previous_writeback_rd = ''
        self.previous_writeback_content = 0

    def stalling_case1(self):
        self.rd_array2.append(self.rd_array1[0])
        if (len(self.rd_array2) == 2):
            self.rd_array2.pop(0)
        self.rd_array1.pop(0)
        self.cycle += 1
        self.stalls += 1
        self.data_hazards += 1
        self.DH_stalls += 1
        self.stalling1 = True

    def stalling_case2(self):
        self.rd_array2.pop(0)
        self.cycle += 1
        self.stalls += 1
        if (self.stalling1 == False):
            self.data_hazards += 1
        self.stalling1 = False
        self.DH_stalls += 1

    def stalling_case3(self):
        self.stalling1 = False
        if (len(self.rd_array1) == 2):
            self.rd_array2.append(self.rd_array1[0])
            if (len(self.rd_array2) == 2):
                self.rd_array2.pop(0)
            self.rd_array1.pop(0)
        if (len(self.rd_array2) == 2):
            self.rd_array2.pop(0)

        if (self.PC <= last_PC + 8):
            self.execute()
            if (self.check_sb_format_execution):
                self.operation1 = ''

            if (
                    self.operation == "bge" or self.operation == "blt" or self.operation == "beq" or self.operation == "bne"):
                self.check_sb_format_execution = self.check_sb_format_execution
            else:
                self.check_sb_format_execution = False

            if (self.PC == last_PC + 8):
                self.PC += 4

        if (self.PC <= last_PC + 4):
            self.decode(self.IF)
            if (
                    self.operation == "lb" or self.operation == "lh" or self.operation == "lw" or self.operation == "sb" or self.operation == "sh" or self.operation == "sw"):
                self.DT_instructions += 1

            elif (
                    self.operation == "beq" or self.operation == "bge" or self.operation == "bne" or self.operation == "blt" or self.operation == "jal" or self.operation == "jalr"):
                self.control_instructions += 1
            else:
                self.ALU_instructions += 1

            self.rd_array1.append(self.rd)
            if (self.PC == last_PC + 4):
                self.PC += 4

        if (self.PC <= last_PC):
            self.fetch(Instruct[self.PC])
            if (self.check_sb_format_execution == True):
                if (self.PC_jumped_count == 8):
                    self.operation = ''
                    self.PC = self.PC_changed_in_sb_format
                elif (self.PC_jumped_count > 8):
                    self.operation = ''
                    self.IF = ''
                    self.PC = self.PC_changed_in_sb_format - 4

        self.cycle += 1

    def data_forwarding_case1(self):
        if (self.rd_array1[0] == self.rs1):  # data_forwarding
            self.rs1_bool = True
            self.rs1_a = pipelining.jot
            self.data_hazards += 1
        if (self.rd_array1[0] == pipelining.rs2):
            self.rs2_bool = True
            self.rs2_b = self.jot
            self.data_hazards += 1

        self.rd_array2.append(self.rd_array1[0])
        if (len(self.rd_array2) == 2):
            self.rd_array2.pop(0)
        self.rd_array1.pop(0)

        if (self.PC <= last_PC + 8):
            self.execute()

            self.rs1_bool = False  # data_forwarding boolean var
            self.rs2_bool = False

            if (self.check_sb_format_execution):
                self.operation1 = ''

            if (
                    self.operation == "bge" or self.operation == "blt" or self.operation == "beq" or self.operation == "bne"):
                self.check_sb_format_execution = self.check_sb_format_execution
            else:
                self.check_sb_format_execution = False

            if (self.PC == last_PC + 8):
                self.PC += 4

        if (self.PC <= last_PC + 4):
            self.decode(self.IF)
            if (
                    self.operation == "lb" or self.operation == "lh" or self.operation == "lw" or self.operation == "sb" or self.operation == "sh" or self.operation == "sw"):
                self.DT_instructions += 1

            elif (
                    self.operation == "beq" or self.operation == "bge" or self.operation == "bne" or self.operation == "blt" or self.operation == "jal" or self.operation == "jalr"):
                self.control_instructions += 1
            else:
                self.ALU_instructions += 1

            self.rd_array1.append(self.rd)
            if (self.PC == last_PC + 4):
                self.PC += 4

        if (self.PC <= last_PC):
            self.fetch(Instruct[self.PC])
            if (self.check_sb_format_execution == True):
                if (self.PC_jumped_count == 8):
                    self.operation = ''
                    self.PC = self.PC_changed_in_sb_format
                elif (self.PC_jumped_count > 8):
                    self.operation = ''
                    self.IF = ''
                    self.PC = self.PC_changed_in_sb_format - 4

        self.cycle += 1

    def data_forwarding_case2(self):
        if (self.rd_array1[0] == self.rs1):  # data_forwarding
            self.rs1_bool = True
            self.rs1_a = self.jot
            self.data_hazards += 1
        if (self.rd_array1[0] == self.rs2):
            self.rs2_bool = True
            self.rs2_b = self.jot
            self.data_hazards += 1

        self.rd_array2.pop(0)
        if (self.PC <= last_PC + 8):
            self.execute()

            self.rs1_bool = False  # data_forwarding boolean var
            self.rs2_bool = False

            if (self.check_sb_format_execution):
                self.operation1 = ''

            if (
                    self.operation == "bge" or self.operation == "blt" or self.operation == "beq" or self.operation == "bne"):
                self.check_sb_format_execution = self.check_sb_format_execution
            else:
                self.check_sb_format_execution = False

            if (self.PC == last_PC + 8):
                self.PC += 4

        if (self.PC <= last_PC + 4):
            self.decode(self.IF)
            if (
                    self.operation == "lb" or self.operation == "lh" or self.operation == "lw" or self.operation == "sb" or self.operation == "sh" or self.operation == "sw"):
                self.DT_instructions += 1

            elif (
                    self.operation == "beq" or self.operation == "bge" or self.operation == "bne" or self.operation == "blt" or self.operation == "jal" or self.operation == "jalr"):
                self.control_instructions += 1
            else:
                self.ALU_instructions += 1

            self.rd_array1.append(self.rd)
            if (self.PC == last_PC + 4):
                self.PC += 4

        if (self.PC <= last_PC):
            self.fetch(Instruct[self.PC])
            if (self.check_sb_format_execution == True):
                if (self.PC_jumped_count == 8):
                    self.operation = ''
                    self.PC = self.PC_changed_in_sb_format
                elif (self.PC_jumped_count > 8):
                    self.operation = ''
                    self.IF = ''
                    self.PC = self.PC_changed_in_sb_format - 4

        self.cycle += 1

    def data_forwarding_case3(self):
        if (len(self.rd_array1) == 2):
            self.rd_array2.append(self.rd_array1[0])
            if (len(self.rd_array2) == 2):
                self.rd_array2.pop(0)
            self.rd_array1.pop(0)

        if (len(self.rd_array2) == 2):
            self.rd_array2.pop(0)

        if (self.PC <= last_PC + 8):
            self.execute()

            if (self.check_sb_format_execution):
                self.operation1 = ''

            if (
                    self.operation == "bge" or self.operation == "blt" or self.operation == "beq" or self.operation == "bne"):
                self.check_sb_format_execution = self.check_sb_format_execution
            else:
                self.check_sb_format_execution = False

            if (self.PC == last_PC + 8):
                self.PC += 4

        if (self.PC <= last_PC + 4):
            self.decode(self.IF)
            if (
                    self.operation == "lb" or self.operation == "lh" or self.operation == "lw" or self.operation == "sb" or self.operation == "sh" or self.operation == "sw"):
                self.DT_instructions += 1

            elif (
                    self.operation == "beq" or self.operation == "bge" or self.operation == "bne" or self.operation == "blt" or self.operation == "jal" or self.operation == "jalr"):
                self.control_instructions += 1
            else:
                self.ALU_instructions += 1

            self.rd_array1.append(self.rd)
            if (self.PC == last_PC + 4):
                self.PC += 4

        if (self.PC <= last_PC):
            self.fetch(Instruct[self.PC])
            if (self.check_sb_format_execution == True):
                if (self.PC_jumped_count == 8):
                    self.operation = ''
                    self.PC = self.PC_changed_in_sb_format
                elif (self.PC_jumped_count > 8):
                    self.operation = ''
                    self.IF = ''
                    self.PC = self.PC_changed_in_sb_format - 4

        self.cycle += 1


# file = open(sys.argv[1], 'r')
# datasegOrnot = 0
Instruct = {}
# for line in file:
#     if (line == "\n"):
#         datasegOrnot = 1
#         continue
#     if (datasegOrnot == 1):  # fetching memory from data segment
#         dataArray = line.split(' ')
#         daata = dataArray[1][2:4]
#         # print(daata)
#         memory[int(dataArray[0], 16)] = daata
#         continue
# file.close()

last_PC = 0
file = open(sys.argv[1], 'r')
for line in file:
    if (line == "\n"):
        break
    inputsArray = line.split(' ')
    tempc = int(inputsArray[0][2:], 16)
    binaryno = bin(int(inputsArray[1][2:], 16))[2:].zfill(32)
    Instruct[tempc] = binaryno
    last_PC = tempc
file.close()

knob1 = int(input("Enter the value of Knob1(0/1): 0 for choosing non-pipelining and 1 for choosing pipelining\n"))
if (knob1 == 1):
    knob2 = int(
        input("Enter the value of Knob2(0/1):0 if pipeline is expected to work with stalling and 1 for data-forwarding\n"))
knob3 = int(input(
    "Enter the value of Knob3(0/1): 0 for not printing and 1 for printing values in register file at the end of each cycle \n"))
if (knob1 == 1):
    knob4 = int(input(
        "Enter the value of Knob4(0/1): 0 for not printing and 1 for printing the information in the pipeline registers at the end of each cycle (similar to tracing).\n"))
    



nDataTransfer = 0
nALU = 0
nCtrlInstr = 0





if (knob1 == 0):
    non_pipelining = five_steps()
    non_pipelining.PC = 0
    while (non_pipelining.PC <= last_PC):
        non_pipelining.fetch(Instruct[non_pipelining.PC])
        non_pipelining.decode(non_pipelining.IF)
        if (
                non_pipelining.operation == "lb" or non_pipelining.operation == "lh" or non_pipelining.operation == "lw" or non_pipelining.operation == "sb" or non_pipelining.operation == "sh" or non_pipelining.operation == "sw"):
            non_pipelining.DT_instructions += 1

        elif (
                non_pipelining.operation == "beq" or non_pipelining.operation == "bge" or non_pipelining.operation == "bne" or non_pipelining.operation == "blt" or non_pipelining.operation == "jal" or non_pipelining.operation == "jalr"):
            non_pipelining.control_instructions += 1
        else:
            non_pipelining.ALU_instructions += 1
        non_pipelining.execute()
        non_pipelining.Memory(non_pipelining.operation, non_pipelining.dataa, non_pipelining.rd, non_pipelining.imm,
                              non_pipelining.address)
        non_pipelining.WriteBack(non_pipelining.rd, non_pipelining.jot)
        if (knob3 == 1):
            for i in range(32):
                print("x[", i, "]=", x[i])
        non_pipelining.cycle += 1
        non_pipelining.ninstructions += 1
        print("\n")

    non_pipelining.cpi = non_pipelining.cycle / non_pipelining.ninstructions
    non_pipelining.stalls = 0
    non_pipelining.data_hazards = 0
    non_pipelining.control_hazards = 0
    non_pipelining.mispredictions = 0
    non_pipelining.DH_stalls = 0
    non_pipelining.CH_stalls = 0

    print("\n")
    # print(x)
    # print(memory)
    # for i in range(0, 32):
    #     print("x[", i, "]=", x[i])
    print("Total number of cycles:", non_pipelining.cycle)
    print("Total instructions executed:", non_pipelining.ninstructions)
    print("CPI:", non_pipelining.cpi)
    print("Number of Data transfer (load and store) instructions executed:", non_pipelining.DT_instructions)
    print("Number of ALU instructions executed:", non_pipelining.ALU_instructions)
    print("Number of control instructions executed:", non_pipelining.control_instructions)
    print("Number of stalls:", non_pipelining.stalls)
    print("Number of data hazards:", non_pipelining.data_hazards)
    print("Number of control hazards:", non_pipelining.control_hazards)
    print("Number of Branch mispredictions:", non_pipelining.mispredictions)
    print("Number of stalls due to data hazards:", non_pipelining.DH_stalls)
    print("Number of stalls due to control hazards:", non_pipelining.CH_stalls)

elif (knob1 == 1):
    if (knob2 == 0):
        pipelining = five_steps()
        pipelining.PC = 0
        while (pipelining.PC <= last_PC + 16):
            if (pipelining.cycle == 0):
                pipelining.fetch(Instruct[pipelining.PC])
                pipelining.cycle += 1
            elif (pipelining.cycle == 1):
                pipelining.decode(pipelining.IF)

                if (
                        pipelining.operation == "lb" or pipelining.operation == "lh" or pipelining.operation == "lw" or pipelining.operation == "sb" or pipelining.operation == "sh" or pipelining.operation == "sw"):
                    pipelining.DT_instructions += 1

                elif (
                        pipelining.operation == "beq" or pipelining.operation == "bge" or pipelining.operation == "bne" or pipelining.operation == "blt" or pipelining.operation == "jal" or pipelining.operation == "jalr"):
                    pipelining.control_instructions += 1
                else:
                    pipelining.ALU_instructions += 1

                pipelining.rd_array1.append(pipelining.rd)
                pipelining.fetch(Instruct[pipelining.PC])

                pipelining.cycle += 1
            elif (pipelining.cycle == 2):
                pipelining.execute()
                pipelining.decode(pipelining.IF)

                if (
                        pipelining.operation == "lb" or pipelining.operation == "lh" or pipelining.operation == "lw" or pipelining.operation == "sb" or pipelining.operation == "sh" or pipelining.operation == "sw"):
                    pipelining.DT_instructions += 1

                elif (
                        pipelining.operation == "beq" or pipelining.operation == "bge" or pipelining.operation == "bne" or pipelining.operation == "blt" or pipelining.operation == "jal" or pipelining.operation == "jalr"):
                    pipelining.control_instructions += 1
                else:
                    pipelining.ALU_instructions += 1

                pipelining.rd_array1.append(pipelining.rd)
                pipelining.fetch(Instruct[pipelining.PC])
                pipelining.cycle += 1
            elif (pipelining.cycle == 3):
                pipelining.save_last_called_memory()
                pipelining.Memory(pipelining.operation1, pipelining.dataa1, pipelining.rd1, pipelining.imm1,
                                  pipelining.address1)
                if (pipelining.rd_array1[0] == pipelining.rs1 or pipelining.rd_array1[0] == pipelining.rs2):
                    pipelining.rd_array2.append(
                        pipelining.rd_array1[0])  # contains rd of instruction2 and array_2 with instruction1
                    pipelining.rd_array1.pop(0)  # No use of rd of instruction1
                    pipelining.cycle += 1
                else:
                    pipelining.execute()
                    pipelining.decode(pipelining.IF)

                    if (
                            pipelining.operation == "lb" or pipelining.operation == "lh" or pipelining.operation == "lw" or pipelining.operation == "sb" or pipelining.operation == "sh" or pipelining.operation == "sw"):
                        pipelining.DT_instructions += 1

                    elif (
                            pipelining.operation == "beq" or pipelining.operation == "bge" or pipelining.operation == "bne" or pipelining.operation == "blt" or pipelining.operation == "jal" or pipelining.operation == "jalr"):
                        pipelining.control_instructions += 1
                    else:
                        pipelining.ALU_instructions += 1

                    pipelining.rd_array1.append(pipelining.rd)  # contains rd of instruction2 and instruction3
                    pipelining.rd_array1.pop(0)  # No use of rd of instruction1
                    pipelining.fetch(Instruct[pipelining.PC])
                    pipelining.cycle += 1
            elif (pipelining.cycle >= 4):

                if (len(pipelining.rd_array2) == 2):
                    pipelining.rd_array2.pop(0)
                if (len(pipelining.rd_array1) == 3):
                    pipelining.rd_array2.append(pipelining.rd_array1[0])
                    pipelining.rd_array1.pop(0)
                if (len(pipelining.rd_array2) == 2):
                    pipelining.rd_array2.pop(0)

                if (pipelining.PC == last_PC + 16):
                    pipelining.PC += 4
                if (pipelining.check_already_called_writeback() == 0):
                    pipelining.save_last_called_writeback()
                    pipelining.WriteBack(pipelining.rd2, pipelining.jot2)
                    pipelining.ninstructions += 1
                if (pipelining.PC <= last_PC + 12):
                    if (pipelining.operation1 != ''):
                        if (pipelining.check_already_called_memory() == 0):
                            pipelining.save_last_called_memory()
                            pipelining.clear_already_called_writeback()

                            pipelining.Memory(pipelining.operation1, pipelining.dataa1, pipelining.rd1, pipelining.imm1,
                                              pipelining.address1)
                    if (pipelining.PC == last_PC + 12):
                        pipelining.PC += 4

                if (len(pipelining.rd_array2) == 0):
                    if (len(pipelining.rd_array1) == 1 or len(pipelining.rd_array1) == 0):
                        pipelining.stalling_case3()
                    else:
                        if (pipelining.rd_array1[0] == pipelining.rs1 or pipelining.rd_array1[0] == pipelining.rs2):
                            pipelining.stalling_case1()
                        else:
                            pipelining.stalling_case3()
                elif (len(pipelining.rd_array2) == 1):
                    if (len(pipelining.rd_array1) == 3 or len(pipelining.rd_array1) == 2):
                        if (pipelining.rd_array1[0] == pipelining.rs1 or pipelining.rd_array1[0] == pipelining.rs2):
                            pipelining.stalling_case1()
                        elif (pipelining.rd_array2[0] == pipelining.rs1 or pipelining.rd_array2[0] == pipelining.rs2):
                            pipelining.stalling_case2()
                        else:
                            pipelining.stalling_case3()
                    else:
                        if (pipelining.rd_array2[0] == pipelining.rs1 or pipelining.rd_array2[0] == pipelining.rs2):
                            pipelining.stalling_case2()
                        else:
                            pipelining.stalling_case3()

            if (knob3 == 1):
                for i in range(32):
                    print("x[", i, "]=", x[i])
            
            if (knob4 == 1):
                print("\nBuffer registers:")
                for j in pipelining.buffer[pipelining.ind]:
                    l=0
                    for k in j:
                        
                        if(l==0):
                            print(k,":",j[k] , end=" ")
                            l+=1
                        else:
                            print(k,":",j[k] , end=", ")
                    print("")
                pipelining.ind+=1

            print("cycle no. ", pipelining.cycle)
            print("\n")

        pipelining.cpi = pipelining.cycle / pipelining.ninstructions
        
        for i in range(32):
            print("x[", i, "]=", x[i])
        

        # print(memory)
    else:
        pipelining = five_steps()
        pipelining.PC = 0
        while (pipelining.PC <= last_PC + 16):
            if (pipelining.cycle == 0):
                pipelining.fetch(Instruct[pipelining.PC])
                pipelining.cycle += 1
            elif (pipelining.cycle == 1):
                pipelining.decode(pipelining.IF)

                if (
                        pipelining.operation == "lb" or pipelining.operation == "lh" or pipelining.operation == "lw" or pipelining.operation == "sb" or pipelining.operation == "sh" or pipelining.operation == "sw"):
                    pipelining.DT_instructions += 1

                elif (
                        pipelining.operation == "beq" or pipelining.operation == "bge" or pipelining.operation == "bne" or pipelining.operation == "blt" or pipelining.operation == "jal" or pipelining.operation == "jalr"):
                    pipelining.control_instructions += 1
                else:
                    pipelining.ALU_instructions += 1

                pipelining.rd_array1.append(pipelining.rd)
                pipelining.fetch(Instruct[pipelining.PC])
                pipelining.cycle += 1
            elif (pipelining.cycle == 2):
                pipelining.execute()
                pipelining.decode(pipelining.IF)

                if (
                        pipelining.operation == "lb" or pipelining.operation == "lh" or pipelining.operation == "lw" or pipelining.operation == "sb" or pipelining.operation == "sh" or pipelining.operation == "sw"):
                    pipelining.DT_instructions += 1

                elif (
                        pipelining.operation == "beq" or pipelining.operation == "bge" or pipelining.operation == "bne" or pipelining.operation == "blt" or pipelining.operation == "jal" or pipelining.operation == "jalr"):
                    pipelining.control_instructions += 1
                else:
                    pipelining.ALU_instructions += 1

                pipelining.rd_array1.append(pipelining.rd)
                pipelining.fetch(Instruct[pipelining.PC])
                pipelining.cycle += 1
            elif (pipelining.cycle == 3):
                pipelining.save_last_called_memory()
                pipelining.Memory(pipelining.operation1, pipelining.dataa1, pipelining.rd1, pipelining.imm1,
                                  pipelining.address1)
                if (pipelining.rd_array1[0] == pipelining.rs1 or pipelining.rd_array1[0] == pipelining.rs2):
                    if (pipelining.rd_array1[0] == pipelining.rs1):  # data_forwarding
                        pipelining.rs1_bool = True
                        pipelining.rs1_a = pipelining.jot
                    if (pipelining.rd_array1[0] == pipelining.rs2):
                        pipelining.rs2_bool = True
                        pipelining.rs2_b = pipelining.jot
                        
                pipelining.execute()
                pipelining.rs1_bool = False  # data_forwarding boolean var
                pipelining.rs2_bool = False
                pipelining.decode(pipelining.IF)

                if (
                        pipelining.operation == "lb" or pipelining.operation == "lh" or pipelining.operation == "lw" or pipelining.operation == "sb" or pipelining.operation == "sh" or pipelining.operation == "sw"):
                    pipelining.DT_instructions += 1

                elif (
                        pipelining.operation == "beq" or pipelining.operation == "bge" or pipelining.operation == "bne" or pipelining.operation == "blt" or pipelining.operation == "jal" or pipelining.operation == "jalr"):
                    pipelining.control_instructions += 1
                else:
                    pipelining.ALU_instructions += 1

                pipelining.rd_array1.append(pipelining.rd)  # contains rd of instruction2 and instruction3
                pipelining.rd_array1.pop(0)  # No use of rd of instruction1
                pipelining.fetch(Instruct[pipelining.PC])
                pipelining.cycle += 1
            elif (pipelining.cycle >= 4):

                if (len(pipelining.rd_array2) == 2):
                    pipelining.rd_array2.pop(0)
                if (len(pipelining.rd_array1) == 3):
                    pipelining.rd_array2.append(pipelining.rd_array1[0])
                    pipelining.rd_array1.pop(0)
                if (len(pipelining.rd_array2) == 2):
                    pipelining.rd_array2.pop(0)

                if (pipelining.PC == last_PC + 16):
                    pipelining.PC += 4
                if (pipelining.check_already_called_writeback() == 0):
                    pipelining.save_last_called_writeback()
                    pipelining.WriteBack(pipelining.rd2, pipelining.jot2)
                    pipelining.ninstructions += 1
                if (pipelining.PC <= last_PC + 12):
                    if (pipelining.operation1 != ''):
                        if (pipelining.check_already_called_memory() == 0):
                            pipelining.save_last_called_memory()
                            pipelining.clear_already_called_writeback()
                            pipelining.Memory(pipelining.operation1, pipelining.dataa1, pipelining.rd1, pipelining.imm1,
                                              pipelining.address1)
                    if (pipelining.PC == last_PC + 12):
                        pipelining.PC += 4

                if (len(pipelining.rd_array2) == 0):
                    if (len(pipelining.rd_array1) == 1 or len(pipelining.rd_array1) == 0):
                        pipelining.data_forwarding_case3()
                    else:
                        if (pipelining.rd_array1[0] == pipelining.rs1 or pipelining.rd_array1[0] == pipelining.rs2):
                            pipelining.data_forwarding_case1()
                        else:
                            pipelining.data_forwarding_case3()
                elif (len(pipelining.rd_array2) == 1):
                    if (len(pipelining.rd_array1) == 3 or len(pipelining.rd_array1) == 2):
                        if (pipelining.rd_array1[0] == pipelining.rs1 or pipelining.rd_array1[0] == pipelining.rs2):
                            pipelining.data_forwarding_case1()
                        elif (pipelining.rd_array2[0] == pipelining.rs1 or pipelining.rd_array2[0] == pipelining.rs2):
                            pipelining.data_forwarding_case2()
                        else:
                            pipelining.data_forwarding_case3()
                    else:
                        if (pipelining.rd_array2[0] == pipelining.rs1 or pipelining.rd_array2[0] == pipelining.rs2):
                            pipelining.data_forwarding_case2()
                        else:
                            pipelining.data_forwarding_case3()

            if (knob3 == 1):
                for i in range(32):
                    print("x[", i, "]=", x[i])
            if (knob4 == 1):
                print("\nBuffer registers:")
                for j in pipelining.buffer[pipelining.ind]:
                    l=0
                    for k in j:
                        
                        if(l==0):
                            print(k,":",j[k] , end=" ")
                            l+=1
                        else:
                            print(k,":",j[k] , end=", ")
                    print("")
                pipelining.ind+=1
            print("cycle no. ", pipelining.cycle)
            print("\n")
        
        # print("cycle no. ", pipelining.cycle)
        # print("\n")

        pipelining.cpi = pipelining.cycle / pipelining.ninstructions
        # print_regi_in_file = open("RegOut.txt", 'w')
        # for i in range(0, 32):
        #     print_regi_in_file.write("x["+str(i)+"]="+str(x[i])+"\n")
        # print_regi_in_file.close()
        # for i in range(0, 32):
        #     print("x[", i, "]=", x[i])
        # print("cycle no. ", pipelining.cycle)
        # print(memory)
        # for j in memory.keys():
        #     print(hex(j),":",memory[j]," (",int(memory[j], 16),")")
        # print_inst=open("Ins.txt",'w')
        # print_inst.write(str(Instruct))
        # print_inst.close()

    print("Total number of cycles:", pipelining.cycle)
    print("Total instructions executed:", pipelining.ninstructions)
    print("CPI:", pipelining.cpi)
    print("Number of Data transfer (load and store) instructions executed:", pipelining.DT_instructions)
    print("Number of ALU instructions executed:", pipelining.ALU_instructions)
    print("Number of control instructions executed:", pipelining.control_instructions)
    print("Number of stalls:", pipelining.stalls)
    print("Number of data hazards:", pipelining.data_hazards)
    print("Number of Branch mispredictions:", pipelining.mispredictions)
    print("Number of stalls due to data hazards:", pipelining.DH_stalls)



print_regi_in_file = open("RegOut.txt", 'w')
for i in range(32):
        print_regi_in_file.write("x["+str(i)+"]="+str(x[i])+"\n")
print_regi_in_file.close()

# for j in memory.keys():
#     print(hex(j),":",memory[j]," (",int(memory[j], 16),")")
print_inst=open("Ins.txt",'w')
for kuch_bhi in Instruct.keys():
    print_inst.write(str(hex(kuch_bhi))+" "+str(Instruct[kuch_bhi])+"\n")
# print_inst.write(str(Instruct))
print_inst.close()
new_file = open("MEM.txt", "w")
# for line in Instruct:
#     new_file.write(str(hex(line)))
#     new_file.write(" 0x")
#     a = hex(int(Instruct[line], 2))[2:].zfill(8)
#     new_file.write(str(a))
#     new_file.write("\n")

# new_file.write("\n")
for line in memory:
    new_file.write(str(hex(line))+" 0x"+memory[line]+"\n")

new_file.close()
