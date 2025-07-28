import random

def obfuscate_hex(hex_str):
    # Valid hex characters
    hex_chars = '0123456789abcdefABCDEF'
    clean_hex = ''.join(c for c in hex_str if c in hex_chars)

    # Weighted character pool: \/ and + less frequent
    weighted_pool = (
        list('ghijklmnopqrstuvwxyz') * 3 +  # higher weight
        ['/', '+']                          # lower weight
    )

    # Pool of fake hex chars (but distinct from the original hex chars in position)
    extra_hex_pool = list('0123456789abcdefABCDEF')

    result = []

    for char in clean_hex:
        # Add original hex char (randomized casing)
        result.append(char.upper() if char.isalpha() and random.random() < 0.5 else char)

        # Inject 1–5 characters: these can be pure non-hex or mixed with hex
        inject = []
        for _ in range(random.randint(1, 5)):
            if random.random() < 0.2:  # % chance to mix in hex within non-hex
                # Always encapsulate hex characters within non-hex chars
                inject.append(random.choice(weighted_pool))  # non-hex part
                for _ in range(random.randint(2, 4)):
                    inject.append(random.choice(extra_hex_pool))  # hex part
                inject.append(random.choice(weighted_pool))  # non-hex part
            else:
                # Add purely non-hex characters
                inject.append(random.choice(weighted_pool))

        # Add the injected characters to the result
        result.extend(inject)

    # Join result into a string
    obfuscated = ''.join(result)

    # Add base64-like padding
    padding_needed = (4 - len(obfuscated) % 4) % 4
    obfuscated += '=' * padding_needed

    return obfuscated

# Example usage
if __name__ == "__main__":
    user_input = input("Enter a hex string: ")
    obfuscated = obfuscate_hex(user_input)
    print("Obfuscated output:")
    print(obfuscated)
