#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <openssl/rsa.h>
#include <openssl/engine.h>

void decrypt(char *pristr, char *pubkey, int padding, char *pub_str)
{
    BIO *bp;
    EVP_PKEY *pkey;
    int crypted_len, n;
    size_t data_len;
    char *data, *dest_p, *p, *last, *decrypt_buf, *dest;
    char buf[128];

    bp = BIO_new_mem_buf((void *)pubkey, -1);
    pkey = PEM_read_bio_PUBKEY(bp, NULL, NULL, NULL);
    BIO_free(bp);

    if (!pkey) {
        fprintf(stderr, "get public key error\n");
        return;
    }

    crypted_len = EVP_PKEY_size(pkey);
    decrypt_buf = malloc(crypted_len + 1);
    if (!decrypt_buf) {
        fprintf(stderr, "decrypt_buf, malloc error\n");
        return;
    }

    base64_decode(pristr, (unsigned char **)&data, &data_len);

    dest = malloc(data_len);
    if (!dest) {
        fprintf(stderr, "dest, malloc error\n");
        free(decrypt_buf);
        return;
    }
    dest_p = dest;

    p = data;
    last = data + data_len;

    do {
        n = last - p;
        if (n > 128) {
            n = 128;
        }

        bzero(buf, sizeof(buf));
        bzero(decrypt_buf, sizeof(decrypt_buf));
        memcpy(buf, p, n);
        p += n;

        crypted_len = RSA_public_decrypt(n, (unsigned char *)buf, decrypt_buf, pkey->pkey.rsa, padding);
        if (crypted_len != -1) {
            memcpy(dest_p, decrypt_buf, crypted_len);
            dest_p += crypted_len;
        }
    } while (last - p > 0);

    *dest_p = 0;
    strcpy(pub_str, dest);
    free(decrypt_buf);
    free(dest);
    free(data);
}


size_t calc_decode_len(const char* b64input) { 
    size_t len = strlen(b64input), padding = 0;

    if (b64input[len - 1] == '=' && b64input[len - 2] == '=') {
        padding = 2;
    } else if (b64input[len - 1] == '=') {
        padding = 1;
    }

    return (size_t) len * 0.75 - padding;
}

int base64_decode(char *b64message, unsigned char **buffer, size_t *len) {
    BIO *bio, *b64;

    int decode_len = calc_decode_len(b64message);
    *buffer = malloc(decode_len);
    if (!*buffer) {
        fprintf(stderr, "buffer, malloc error\n");
        return -1;
    }

    bio = BIO_new_mem_buf(b64message, -1);
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_push(b64, bio);

    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); 
    *len = BIO_read(bio, *buffer, strlen(b64message));
    BIO_free_all(bio);

    if (*len != decode_len) {
        return -1;
    }

    return 0; 
}

