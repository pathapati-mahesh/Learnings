namespace ControlStatExercises
{
    public class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Enter a Number :");
            int number = Convert.ToInt32(Console.ReadLine());
            int digit2=Convert.ToInt32(Console.ReadLine());
            string message=VerifyUserIp(number);
            Console.WriteLine(message);
            
            string BigNumber=MaxOfTwo(number, digit2);
            Console.WriteLine(BigNumber);

            Console.WriteLine($"{CountNumbers()}");
            
        }
        /*
         Write a program and ask the user to enter a number. The number should be between 1 to 10. 
        If the user enters a valid number, display "Valid" on the console. Otherwise, display "Invalid". 
        (This logic is used a lot in applications where values entered into input boxes need to be validated.)
         */
        public static string VerifyUserIp(int ip) {
            if (ip > 1 && ip < 10)
            {
                return "Valid";
            }
            else {
                return "Invalid";
            }
        }
        /*
         Write a program which takes two numbers from the console and displays the maximum of the two
         */
        public static string MaxOfTwo(int a,int b)
        {
            if (a > b)
            {
                return $"{a} is Greater than {b}";
            }
            else
            {
                return $"{b} is Greater than {a}";
            }
        }
        /*our job is to write a program for a speed camera. 
         * For simplicity, ignore the details such as camera, sensors, etc and focus purely on the logic.
         * Write a program that asks the user to enter the speed limit. Once set, the program asks for the speed of a car.
         * If the user enters a value less than the speed limit, program should display Ok on the console. 
         * If the value is above the speed limit, the program should calculate the number of demerit points.
         * For every 5km/hr above the speed limit, 1 demerit points should be incurred and displayed on the console.
         * If the number of demerit points is above 12, the program should display License Suspended.*/
//public int CalculateDemeritPoints()
//{
//    int DemeritPoints;
//    Console.WriteLine("Enter the speed Limit :");
//    int carSpeed=Convert.ToInt32(Console.ReadLine());
//    if (carSpeed > 80) 
//    {
//        DemeritPoints = carSpeed / 5;

//    }
//}
/* Write a program to count how many numbers between 1 and 100 are divisible by 3 with no remainder.
 Display the count on the console.*/
        public static int CountNumbers()
        {
            int count = 0;
            for (int i = 0; i <= 100;i++)
            {
                if (i % 3 == 0)
                {
                    count += 1;
                }
            }
            return count;
        }



    }
}
