import os
import timeit
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def benchmark_aes_gcm(data_size_bytes, iterations=1000):
    test_payload = os.urandom(data_size_bytes)
    secret_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(secret_key)
    nonce = os.urandom(12)

    def encryption_run():
        aesgcm.encrypt(nonce, test_payload, None)

    ciphertext = aesgcm.encrypt(nonce, test_payload, None)

    def decryption_run():
        aesgcm.decrypt(nonce, ciphertext, None)

    enc_total_time = timeit.timeit(encryption_run, number=iterations)
    dec_total_time = timeit.timeit(decryption_run, number=iterations)

    enc_avg_micro = (enc_total_time / iterations) * 1_000_000
    dec_avg_micro = (dec_total_time / iterations) * 1_000_000

    total_data_mb = (data_size_bytes * iterations) / (1024 * 1024)
    enc_throughput = total_data_mb / enc_total_time
    dec_throughput = total_data_mb / dec_total_time

    return {
        "size_bytes": data_size_bytes,
        "enc_time": enc_avg_micro,
        "dec_time": dec_avg_micro,
        "enc_speed": enc_throughput,
        "dec_speed": dec_throughput
    }

if __name__ == "__main__":
    test_cases = [
        ("Small Payload (Message String)", 34),
        ("Medium Payload (Document Buffer)", 10240),
        ("Large Payload (File Simulation)", 1048576)
    ]

    print("--- AES-256-GCM Performance Benchmark ---")
    print(f"System Environment: Executing 1,000 iterations per tier\n")

    for title, size in test_cases:
        runs = 100 if size > 500000 else 1000
        metrics = benchmark_aes_gcm(size, iterations=runs)
        
        print(f"📋 Tier: {title} [{size:,} Bytes]")
        print(f"   -> Avg Encryption Time: {metrics['enc_time']:10.2f} μs | Throughput: {metrics['enc_speed']:8.2f} MB/s")
        print(f"   -> Avg Decryption Time: {metrics['dec_time']:10.2f} μs | Throughput: {metrics['dec_speed']:8.2f} MB/s\n")
