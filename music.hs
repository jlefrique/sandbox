firstOctave :: [Float]
firstOctave = map (\n -> baseFrequency * (2 ** (n / 12))) [0..11]
    where baseFrequency = 32.70 :: Float

octave :: Int -> [Float]
octave n = if n == 0
    then firstOctave
    else map (*2) (octave (n - 1))

displayOctave :: Int -> IO ()
displayOctave n = putStrLn $ unwords ["Octave", show n, "=", show (octave n)]

main = do
    displayOctave 0
    displayOctave 1
    displayOctave 2
