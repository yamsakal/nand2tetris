// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// i = R0
@0
D=M
@i
M=D 

// num = R1
@1
D=M
@num
M=D

// sum = 0
@sum
M=0

(LOOP)
    // while(i != 0)
    @i
    D=M
    @END
    D;JEQ

    // sum += num
    @num
    D=M
    @sum
    M=D+M
    
    // i--
    @i
    M=M-1

    @LOOP
    0;JMP
(END)
    // R2 = sum
    @sum
    D=M
    @2
    M=D
