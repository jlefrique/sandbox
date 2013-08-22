primes :: [Integer]
primes = 2 : filter isPrime [3,5..]

isPrime :: Integer -> Bool
isPrime n = all (\x -> n `rem` x /= 0) candidates
    where candidates = takeWhile (\x -> x*x <= n) primes

main = do
    print $ isPrime 2
    print $ isPrime 3
    print $ isPrime 4
    print $ isPrime 7
    print $ isPrime 10
