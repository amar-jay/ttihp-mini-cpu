# miniCPU – Minimal 8-bit Accumulator CPU

## Overview

miniCPU is a minimal 8-bit accumulator-based processor designed for **Tiny Tapeout ASIC fabrication**.
It implements a compact custom ISA and executes a small program that generates a visually observable LED pattern (Knight Rider-style scanner).

The design emphasizes:

* Minimal area usage
* Clean synchronous architecture
* Simple, deterministic behavior
* Easy-to-understand instruction set

---

## Features

* 8-bit accumulator (`A`)
* 8-bit secondary register (`B`)
* 5-bit program counter (32 instructions)
* 8-bit output register (drives `uo_out`)
* 16-cycle clock divider for visible output timing
* Custom 8-bit instruction format

---

## Instruction Set Architecture (ISA)

### Instruction Format

```
[7:5] Opcode | [4:0] Operand
```

### Core Instructions

| Opcode | Mnemonic  | Description                 |
| ------ | --------- | --------------------------- |
| 000    | LDI imm5  | A = imm5                    |
| 001    | ADDI imm5 | A = A + imm5                |
| 010    | SUBI imm5 | A = A - imm5                |
| 011    | ALU ops   | Register / logic operations |
| 100    | OUT       | Output A to pins            |
| 101    | JNZ       | Jump if A ≠ 0               |
| 110    | JZ        | Jump if A = 0               |
| 111    | JMP       | Unconditional jump          |

### ALU Sub-operations (opcode 011)

| Sub-op | Function       |
| ------ | -------------- |
| 0000   | TAB (B = A)    |
| 0001   | TBA (A = B)    |
| 0010   | IN (A = ui_in) |
| 0011   | AND            |
| 0100   | OR             |
| 0101   | XOR            |
| 0110   | ADD            |
| 0111   | SUB            |
| 1000   | SHL            |
| 1001   | SHR            |

---

## Program Behavior

The included ROM program implements a **bidirectional LED scanning pattern**:

1. Load value 1 into accumulator
2. Shift left until overflow
3. Reverse direction using shift right
4. Repeat continuously

This creates a **Knight Rider-style sweeping LED effect** on `uo_out[7:0]`.

---

## Architecture

* Single-cycle FSM CPU with clock enable
* Combinational ALU producing `next_a`
* Synchronous register updates on enabled clock edges
* ROM implemented as combinational case statement
* 4-bit clock divider for human-visible timing

---

## I/O Mapping

* `ui_in`: Input port (read via IN instruction)
* `uo_out`: Output LED pattern (from OUT instruction)
* `uio_*`: Disabled (not used)

---

## Design Philosophy

This CPU is intentionally minimal:

* No pipelining
* No cache or memory hierarchy
* No microcode ROM
* No interrupts

It is designed to demonstrate how **complex behavior can emerge from a very small instruction set and datapath**.

---

### How to test (recommended)

1. Apply reset (`rst_n = 0`) for at least 10 clock cycles
2. Release reset (`rst_n = 1`)
3. Provide a clock signal (e.g., 100 kHz or slower for visibility)
4. Observe `uo_out[7:0]`

### Expected behavior

The output should show a shifting LED pattern:

* A single “1” bit moves from LSB → MSB
* Then reverses direction from MSB → LSB
* This repeats continuously

### Example sequence on `uo_out`

```
00000001
00000010
00000100
00001000
00010000
00100000
01000000
10000000
01000000
00100000
...
```

### Optional input test

* `ui_in[0]` is read by the CPU using the IN instruction
* You can toggle it to verify input responsiveness (if enabled in program flow)

### Cocotb simulation

Run the provided testbench:

```bash
make test
```

This verifies:

* correct reset behavior
* correct output sequence
* correct looping execution

---

## External hardware

No external hardware is required for this project.

The design is fully self-contained and operates entirely using the Tiny Tapeout standard I/O:

uo_out[7:0]: **Drives external LEDs** (recommended for visualization)
ui_in[7:0]: **Optional digital input switches** (not required for basic operation)
uio_*: Not used (bidirectional pins disabled)
Recommended optional setup

To observe behavior more clearly during bring-up:

8× LEDs connected to uo_out[7:0]
8× switches connected to ui_in[7:0] (optional experimentation)

No PMODs, displays, or additional components are required.


---

## Author

[amarjay](https://github.com/amar-jay)

