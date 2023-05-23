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

// r = 256
(MAIN)
    (BLACK)
        @256
        D=A
        @r
        M=D

        // currentindex = 16384
        @16384
        D=A
        @currentindex
        M=D

        (LOOP_BLACK)
            // while(r != 0)
            @r
            D=M
            @END
            D;JEQ

            @32
            D=A
            @c
            M=D
            (COL_LOOP_BLACK)
                // while(c != 0)
                @c
                D=M
                @COL_END_BLACK
                D;JEQ


                // black or white
                @24576
                D=M
                @WHITE
                D;JEQ
            
                // ACTION
                @currentindex
                A=M
                M=-1
                
                // currentindex++
                @currentindex
                D=M+1
                M=D


                // c--
                @c
                M=M-1

                @COL_LOOP_BLACK
                0;JMP
            (COL_END_BLACK)
            // r--
            @r
            M=M-1

            @LOOP_BLACK
            0;JMP
        (END)


    (WHITE)
        @256
        D=A
        @r
        M=D

        // currentindex = 16384
        @16384
        D=A
        @currentindex
        M=D

        (LOOP_WHITE)
            // while(r != 0)
            @r
            D=M
            @END
            D;JEQ

            @32
            D=A
            @c
            M=D
            (COL_LOOP_WHITE)
                // while(c != 0)
                @c
                D=M
                @COL_END_WHITE
                D;JEQ

                // black or white
                @24576
                D=M
                @BLACK
                D;JNE
            
                // ACTION
                @currentindex
                A=M
                M=0
                
                // currentindex++
                @currentindex
                D=M+1
                M=D


                // c--
                @c
                M=M-1

                @COL_LOOP_WHITE
                0;JMP
            (COL_END_WHITE)
            // r--
            @r
            M=M-1

            @LOOP_WHITE
            0;JMP
        (END)
@MAIN
0;JMP
