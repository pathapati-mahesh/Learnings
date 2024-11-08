using System;

namespace ArraysExamples
{
    public class ArraySession
    {
        public int LearnArrays()
        {
            int[] Age = new int[3];
            Age = [1, 2, 3];
            Console.WriteLine(Age[0]);
            return Age[0];
        }
        public void RotateArray() {
            int[] Age = new int[3];
            Age= [1, 2, 3];
            for (int i = 0; i < Age.Length; i++) {
                Console.WriteLine(Age[i]);
            }
        }

    }
}
