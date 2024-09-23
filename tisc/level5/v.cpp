void process_data(uint64_t input_val, char *buffer, uint64_t param_3, char *output) {
    uint32_t *data_ptr;
    char temp_char;
    uint64_t modified_val;
    uint64_t temp_val;
    uint32_t port_val;
    uint32_t data_val;
    uint8_t temp_byte;
    uint64_t combined_val;
    longlong *long_ptr;
    int *stack_ptr;
    uint8_t temp_buf[118];
    uint8_t *port_byte;
    char *char_ptr;

    // Combine high byte of input with a memory value
    modified_val = (uint64_t)CONCAT11((char)(input_val >> 8) + *(char *)(unaff_RBP + 0x20c002), (uint8_t)input_val);
    temp_val = (input_val & 0xffffffffffff0000) | modified_val;

    // Read data from port 0x4E
    port_val = in(0x4e);
    port_byte = (uint8_t *)(uint64_t)port_val;

    // Modify data at a specific location in memory
    data_ptr = (uint32_t *)(port_byte + unaff_RBP * 8 - 0x80);
    data_val = *data_ptr;
    *data_ptr = *data_ptr + (uint32_t)unaff_RDI;

    // Write port data into memory
    temp_byte = (uint8_t)port_val;
    *unaff_RDI = temp_byte;

    // Manipulate another memory location
    char_ptr = (char *)(temp_val + 0x20c0f75c);
    *char_ptr = *char_ptr + temp_byte + CARRY4(data_val, (uint32_t)unaff_RDI);

    // Modify memory at another offset
    char_ptr = (char *)(temp_val - 0x3fedf3fe);
    *char_ptr = *char_ptr + (char)(modified_val >> 8);
    *port_byte = *port_byte & temp_byte;

    // Update long pointer with modified input
    long_ptr = (longlong *)(input_val & 0xffffffffffff0000 | (modified_val & 0xffffffffffffff00) | ((uint8_t)input_val & port_byte[1]));
    *long_ptr = *long_ptr + (longlong)unaff_RSI;

    // Update stack data with input
    *stack_ptr = *stack_ptr + (char)((uint64_t)stack_ptr >> 8);
    temp_buf[CONCAT71(unaff_00000019, unaff_BL) * 4] = temp_buf[CONCAT71(unaff_00000019, unaff_BL) * 4] & (uint8_t)((uint64_t)buffer >> 8);

    // Further data manipulation and updates
    combined_val = (uint64_t)(uint32_t)((int)stack_ptr + *stack_ptr);
    data_val = (int)stack_ptr + 0xee7d1ffc;
    *(uint32_t *)((longlong)long_ptr - 9) &= (uint32_t)buffer;

    // Modify buffer
    temp_char = (char)data_val;
    char_ptr = (char *)(uint64_t)(data_val & 0xffff0000 | (uint32_t)CONCAT11(*buffer, temp_char));
    *buffer = *buffer - temp_char;
    temp_char = *buffer;
    *char_ptr = *char_ptr;

    // Check condition and handle bad data
    if (long_ptr == (longlong *)&A || temp_char == '\0') {
        DAT_ffffffffe2082ad2 += (unaff_BL & (uint8_t)((modified_val & 0xffffffffffffff00) >> 8));
        *(uint64_t *)(combined_val - 8) = *unaff_RSI;
        *output = *output + (char)(combined_val - 8);
        halt_baddata();  // Handle bad data
    }

    // Lock and update
    LOCK();
    *char_ptr = *char_ptr + temp_char;
    cRam0008e0f7208164a0 = temp_char;
    halt_baddata();  // Handle bad data
}