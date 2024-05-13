use rand::rngs::OsRng;
use primal::is_prime;
use rand::Rng;

fn main() {
    let (e, d, n) = generate_keys(32);
    println!("Public Key: (e: {}, n: {})", e, n);
    println!("Private Key: (d: {}, n: {})", d, n);

    if let Some(computed_d) = compute_private_key(e, n) {
        println!("Computed Private Key: (d: {}, n: {})", computed_d, n);
    } else {
        println!("Failed to compute private key.");
    }
}

fn generate_keys(bits: u32) -> (u64, u64, u64) {
    let mut p: u64;
    let mut q: u64;
    let e: u64 = 65537;

    loop {
        p = generate_prime(bits / 2);
        q = generate_prime(bits / 2);
        if p != q {
            break;
        }
    }

    let n = p * q;
    let phi = (p - 1) * (q - 1);
    let d = modinv(e, phi).expect("Modular inverse does not exist.");

    (e, d, n)
}

fn generate_prime(bits: u32) -> u64 {
    let mut rng = OsRng;
    loop {
        let num = rng.gen_range((1u64 << (bits - 1))..(1u64 << bits));
        if is_prime(num as u64) {
            return num;
        }
    }
}

fn modinv(a: u64, module: u64) -> Option<u64> {
    let mut mn = (module, a);
    let mut xy = (0u64, 1u64);

    while mn.1 != 0 {
        let quotient = mn.0 / mn.1;
        xy = (xy.1, xy.0.wrapping_sub(quotient.wrapping_mul(xy.1)));
        mn = (mn.1, mn.0 % mn.1);
    }

    if mn.0 > 1 { return None; }
    Some((xy.0.wrapping_add(module)) % module)
}


fn compute_private_key(e: u64, n: u64) -> Option<u64> {
    if let Some((p, q)) = factor_modulus(n) {
        let phi = (p - 1) * (q - 1);
        return modinv(e, phi);
    }
    None
}

fn factor_modulus(n: u64) -> Option<(u64, u64)> {
    for i in 2..(n as f64).sqrt() as u64 + 1 {
        if n % i == 0 && is_prime(i as u64) {
            let j = n / i;
            if is_prime(j as u64) {
                return Some((i, j));
            }
        }
    }
    None
}
