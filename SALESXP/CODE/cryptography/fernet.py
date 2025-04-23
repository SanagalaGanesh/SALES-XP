class FernetCipher:
    def __init__(self, key):
        # Ensure key is exactly 16 bytes
        if isinstance(key, str):
            key = key.encode('utf-8')
        if len(key) < 16:
            key = key + b'\x00' * (16 - len(key))
        elif len(key) > 16:
            key = key[:16]
        self.key = key
        self.block_size = 16
        self.iv = b'\x00' * 16
        # S-box and inverse S-box for substitution
        self.sbox = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]
        self.inv_sbox = [
            0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
            0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
            0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
            0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
            0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
            0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
            0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
            0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
            0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
            0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
            0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
            0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
            0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
            0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
        ]
        self.rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    def _sub_bytes(self, state):
        return [self.sbox[b] for b in state]

    def _inv_sub_bytes(self, state):
        return [self.inv_sbox[b] for b in state]

    def _shift_rows(self, state):
        return [
            state[0], state[5], state[10], state[15],
            state[4], state[9], state[14], state[3],
            state[8], state[13], state[2], state[7],
            state[12], state[1], state[6], state[11]
        ]

    def _inv_shift_rows(self, state):
        return [
            state[0], state[13], state[10], state[7],
            state[4], state[1], state[14], state[11],
            state[8], state[5], state[2], state[15],
            state[12], state[9], state[6], state[3]
        ]

    def _mix_columns(self, state):
        def gf_mult(a, b):
            p = 0
            for _ in range(8):
                if b & 1:
                    p ^= a
                hi_bit_set = a & 0x80
                a <<= 1
                if hi_bit_set:
                    a ^= 0x1b
                b >>= 1
            return p & 0xff

        new_state = [0] * 16
        for i in range(0, 16, 4):
            new_state[i] = gf_mult(2, state[i]) ^ gf_mult(3, state[i+1]) ^ state[i+2] ^ state[i+3]
            new_state[i+1] = state[i] ^ gf_mult(2, state[i+1]) ^ gf_mult(3, state[i+2]) ^ state[i+3]
            new_state[i+2] = state[i] ^ state[i+1] ^ gf_mult(2, state[i+2]) ^ gf_mult(3, state[i+3])
            new_state[i+3] = gf_mult(3, state[i]) ^ state[i+1] ^ state[i+2] ^ gf_mult(2, state[i+3])
        return new_state

    def _inv_mix_columns(self, state):
        def gf_mult(a, b):
            p = 0
            for _ in range(8):
                if b & 1:
                    p ^= a
                hi_bit_set = a & 0x80
                a <<= 1
                if hi_bit_set:
                    a ^= 0x1b
                b >>= 1
            return p & 0xff

        new_state = [0] * 16
        for i in range(0, 16, 4):
            new_state[i] = gf_mult(0x0e, state[i]) ^ gf_mult(0x0b, state[i+1]) ^ gf_mult(0x0d, state[i+2]) ^ gf_mult(0x09, state[i+3])
            new_state[i+1] = gf_mult(0x09, state[i]) ^ gf_mult(0x0e, state[i+1]) ^ gf_mult(0x0b, state[i+2]) ^ gf_mult(0x0d, state[i+3])
            new_state[i+2] = gf_mult(0x0d, state[i]) ^ gf_mult(0x09, state[i+1]) ^ gf_mult(0x0e, state[i+2]) ^ gf_mult(0x0b, state[i+3])
            new_state[i+3] = gf_mult(0x0b, state[i]) ^ gf_mult(0x0d, state[i+1]) ^ gf_mult(0x09, state[i+2]) ^ gf_mult(0x0e, state[i+3])
        return new_state

    def _add_round_key(self, state, round_key):
        return [state[i] ^ round_key[i] for i in range(16)]

    def _key_expansion(self):
        expanded_key = list(self.key)
        for i in range(16, 176, 4):
            temp = expanded_key[i-4:i]
            if i % 16 == 0:
                temp = [self.sbox[temp[1]] ^ self.rcon[i//16-1], self.sbox[temp[2]], self.sbox[temp[3]], self.sbox[temp[0]]]
            for j in range(4):
                expanded_key.append(expanded_key[i-16+j] ^ temp[j])
        return expanded_key

    def _xor_bytes(self, a, b):
        return bytes(x ^ y for x, y in zip(a, b))

    def _base64_encode(self, data):
        base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        result = bytearray()
        for i in range(0, len(data), 3):
            chunk = data[i:i+3]
            n = 0
            for j, byte in enumerate(chunk):
                n |= byte << (16 - 8 * j)
            padding = 3 - len(chunk)
            if padding > 0:
                chunk += b'\x00' * padding
            result.extend(bytes([
                ord(base64_chars[(n >> 18) & 0x3F]),
                ord(base64_chars[(n >> 12) & 0x3F]),
                ord(base64_chars[(n >> 6) & 0x3F]) if padding < 2 else ord('='),
                ord(base64_chars[n & 0x3F]) if padding < 1 else ord('='),
            ]))
        return bytes(result)

    def _base64_decode(self, data):
        base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        result = bytearray()
        for i in range(0, len(data), 4):
            chunk = data[i:i+4]
            n = 0
            padding = 0
            for j, c in enumerate(chunk):
                if c == ord('='):
                    padding = 4 - j
                    break
                n |= base64_chars.index(chr(c)) << (18 - 6 * j)
            result.append((n >> 16) & 0xFF)
            if padding < 2:
                result.append((n >> 8) & 0xFF)
            if padding < 1:
                result.append(n & 0xFF)
        return bytes(result)

    def encrypt(self, data):
        # Convert input to bytes and pad
        if isinstance(data, (int, float)):
            data = str(data)
        if isinstance(data, str):
            data = data.encode('utf-8')
        if len(data) % 16 != 0:
            data += b'\x00' * (16 - len(data) % 16)

        expanded_key = self._key_expansion()
        round_keys = [expanded_key[j:j+16] for j in range(0, 176, 16)]
        encrypted = bytearray()
        prev_block = self.iv

        # Encrypt in CBC mode
        for i in range(0, len(data), 16):
            state = list(self._xor_bytes(data[i:i+16], prev_block))
            
            # Initial round
            state = self._add_round_key(state, round_keys[0])
            
            # 9 main rounds
            for round_num in range(1, 10):
                state = self._sub_bytes(state)
                state = self._shift_rows(state)
                state = self._mix_columns(state)
                state = self._add_round_key(state, round_keys[round_num])
            
            # Final round
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._add_round_key(state, round_keys[10])
            
            encrypted.extend(state)
            prev_block = bytes(state)

        # Mimic Fernet format: version (1 byte) + timestamp (8 bytes) + IV (16 bytes) + ciphertext
        version = b'\x80'  # Fernet version
        timestamp = b'\x00\x00\x00\x00\x00\x00\x00\x01'  # Fixed timestamp
        token = version + timestamp + self.iv + encrypted
        
        # Ensure token length is a multiple of 3 for base64 encoding
        if len(token) % 3 != 0:
            token += b'\x00' * (3 - len(token) % 3)
        
        return self._base64_encode(token)

    def decrypt(self, encrypted_data):
        # Decode base64
        decoded = self._base64_decode(encrypted_data)
        
        # Check if decoded data is long enough
        if len(decoded) < 25:
            raise ValueError("Invalid encrypted data: too short")
        
        # Extract components (skip version and timestamp, use fixed IV)
        ciphertext = decoded[25:]  # Skip version (1) + timestamp (8) + IV (16)

        # Trim any padding added for base64 alignment
        if len(ciphertext) % 16 != 0:
            ciphertext = ciphertext[:-(len(ciphertext) % 16)]

        expanded_key = self._key_expansion()
        round_keys = [expanded_key[j:j+16] for j in range(0, 176, 16)]
        decrypted = bytearray()
        prev_block = self.iv

        # Decrypt in CBC mode
        for i in range(0, len(ciphertext), 16):
            state = list(ciphertext[i:i+16])
            
            # Initial round (inverse of final round)
            state = self._add_round_key(state, round_keys[10])
            state = self._inv_shift_rows(state)
            state = self._inv_sub_bytes(state)
            
            # 9 main rounds
            for round_num in range(9, 0, -1):
                state = self._add_round_key(state, round_keys[round_num])
                state = self._inv_mix_columns(state)
                state = self._inv_shift_rows(state)
                state = self._inv_sub_bytes(state)
            
            # Final round
            state = self._add_round_key(state, round_keys[0])
            
            plaintext_block = self._xor_bytes(bytes(state), prev_block)
            decrypted.extend(plaintext_block)
            prev_block = ciphertext[i:i+16]

        return decrypted.rstrip(b'\x00').decode('utf-8')

# Example usage
def main():
    key = "_secret_key_here"
    print(f"Using key: {key[:16]}")
    cipher = FernetCipher(key)
    
    data = input("Enter the data to encrypt (text, number, or float): ")
    encrypted = cipher.encrypt(data)
    decrypted = cipher.decrypt(encrypted)

    print("\nEncryption and Decryption Results:")
    print("-" * 40)
    print(f"Original: {data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print("-" * 40)

if __name__ == "__main__":
    main()