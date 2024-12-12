package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"fmt"
	"math/rand"
	"os/exec"
	"strconv"
	"strings"
)

func getSeed() (int64, string, error) {
	cmd := exec.Command(
		"curl",
		"-i", "-s", "-k", "-X", "GET",
		"-H", "Host: localhost:9200",
		"-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
		"-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"-H", "Accept-Language: en-US,en;q=0.5",
		"-H", "Accept-Encoding: gzip, deflate",
		"-H", "Dnt: 1",
		// This is the encoded 'oKHzjZw0EGcRxT2cux5K' found password
		"-H", "Authorization: Basic ZWxhc3RpYzpvS0h6alp3MEVHY1J4VDJjdXg1Sw==",
		"-H", "Upgrade-Insecure-Requests: 1",
		"-H", "Sec-Fetch-Dest: document",
		"-H", "Sec-Fetch-Mode: navigate",
		"-H", "Sec-Fetch-Site: none",
		"-H", "Sec-Fetch-User: ?1",
		"-H", "Te: trailers",
		"-H", "Connection: close",
		"-b", "i_like_gitea=1bcfba2fb61ea525; lang=en-US",
		"https://localhost:9200/_search?q=*&pretty=true",
	)

	output, err := cmd.CombinedOutput()
	if err != nil {
		return 0, "", nil
	}

	outputLines := strings.Split(string(output), "\n")
	var seedStr string
	for _, line := range outputLines {
		if strings.Contains(line, "seed") && !strings.Contains(line, "index") {
			seedStr = strings.TrimSpace(strings.Split(line, ":")[1])
			break
		}
	}

	seed, err := strconv.ParseInt(seedStr, 10, 64)
	if err != nil {
		return 0, "", nil
	}

	outputLines = strings.Split(string(output), "\n")
	var blob string
	for _, line := range outputLines {
		if strings.Contains(line, "blob") {
			blob = line
			blob = strings.TrimSpace(strings.Split(line, ":")[1])
			blob = strings.Split(blob, "\"")[1]
			break
		}
	}

	return seed, blob, nil
}

func generateKey(seed int64) []byte {
	rand.Seed(seed)
	key := make([]byte, 16)
	for i := range key {
		key[i] = byte(1 + rand.Intn(254))
	}
	return key
}

func decryptCFB(iv, ciphertext, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	stream := cipher.NewCFBDecrypter(block, iv)
	plaintext := make([]byte, len(ciphertext))
	stream.XORKeyStream(plaintext, ciphertext)

	return plaintext, nil
}

func main() {
	seed, encryptedBlob, _ := getSeed()

	key := generateKey(seed)

	decodedBlob, err := base64.URLEncoding.DecodeString(encryptedBlob)
	if err != nil {
		fmt.Println("Error decoding base64:", err)
		return
	}

	iv := decodedBlob[:aes.BlockSize]
	encryptedData := decodedBlob[aes.BlockSize:]

	decryptedData, err := decryptCFB(iv, encryptedData, key)
	if err != nil {
		fmt.Println("Error decrypting data:", err)
		return
	}

	fmt.Printf("Key: %x\n", key)
	fmt.Printf("IV: %x\n", iv)
	fmt.Printf("Encrypted Data: %x\n", encryptedData)
	fmt.Printf("Decrypted Data: %s\n", decryptedData)
}
