import cocotb
from cocotb.triggers import Timer
from cocotb.handle import Force

@cocotb.test()
async def test_force(dut):
    dut.user_project.instr.value = Force(0xAB)
    await Timer(10, "ns")
    dut._log.info(f"Instr: {hex(int(dut.user_project.instr.value))}")
    # this is used for debug testing. It should be ignored in the final review.
