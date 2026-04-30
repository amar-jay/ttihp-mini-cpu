import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles

@cocotb.test()
async def test_knight_rider(dut):
    dut._log.info("Start robust event-based test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # --- Reset Sequence ---
    dut._log.info("Resetting...")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut._log.info("Reset complete.")

    # The exact expected sequence of outputs (Knight Rider scanner)
    # Forward: 1 -> 128
    # Reverse: 64 -> 1
    expected_sequence = [
        1, 2, 4, 8, 16, 32, 64, 128,
        64, 32, 16, 8, 4, 2, 1
    ]
    
    sequence_index = 0
    prev_val = None
    
    # Track outputs dynamically rather than cycle counting rigidly
    # This prevents failures if clock dividers or latencies change
    
    max_cycles = 10000  # Safety timeout (expecting roughly 2000 cycles max)
    
    for cycle in range(max_cycles):
        await FallingEdge(dut.clk)
        
        current_val = int(dut.uo_out.value)
        
        # Output changed to a valid LED state
        if current_val != prev_val and current_val != 0:
            dut._log.info(f"Got output: {current_val} (Expected: {expected_sequence[sequence_index]})")
            
            assert current_val == expected_sequence[sequence_index], \
                f"Mismatch at index {sequence_index}! Expected {expected_sequence[sequence_index]}, got {current_val}"
            
            sequence_index += 1
            prev_val = current_val
            
            # Did we finish traversing the whole sequence?
            if sequence_index == len(expected_sequence):
                dut._log.info("Full Knight Rider scanner sequence naturally validated!")
                return # Test passes!
                
    # If we exit the loop without returning, the test timed out
    assert False, f"Test timed out before finishing sequence! Stuck at index {sequence_index}/{len(expected_sequence)}."
