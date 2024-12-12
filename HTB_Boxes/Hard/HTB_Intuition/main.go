package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
)

// Calculate MD5 hash
func getMD5Hash(text string) string {
	hash := md5.Sum([]byte(text))
	return hex.EncodeToString(hash[:])
}

// Brute force MD5 hash
func bruteForceMatch(pattern string, targetHash string, position int) string {
	charset := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789|\\@#%&/()=?_.,"
	if position >= len(pattern) {
		if getMD5Hash(pattern) == targetHash {
			return pattern
		}
		return ""
	}

	if pattern[position] != '*' {
		return bruteForceMatch(pattern, targetHash, position+1)
	}

	for _, char := range charset {
		newPattern := pattern[:position] + string(char) + pattern[position+1:]
		result := bruteForceMatch(newPattern, targetHash, position+1)
		if result != "" {
			return result
		}
	}

	return ""
}

// Main
func main() {
	targetHash := "0feda17076d793c2ef2870d7427ad4ed" // Auth hash
	pattern := "UHI75GHI****" // String to find

	result := bruteForceMatch(pattern, targetHash, 0)
	if result != "" {
		fmt.Printf("Match found: %s\n", result)
	} else {
		fmt.Println("No match found.")
	}
}
