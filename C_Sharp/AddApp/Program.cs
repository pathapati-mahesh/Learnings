using System;
using System.Security.AccessControl;

namespace BasicProgram
{
    class AddApp
    {
        static int overflow()
        {
            int maxInt = int.MaxValue;
            int overflowedValue = maxInt + 1;
            return overflowedValue;
        }

        static void Main(String[] args)
        {
            Console.WriteLine($"Adding Two Numbers :{2 + 3}");
            int value=overflow();
            Console.WriteLine($"Over flow Value is :{value}");
        }
    }
}