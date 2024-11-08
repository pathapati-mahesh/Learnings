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
        public void RotateArray()
        {
            int[] Age = new int[3];
            for (int j = 0; j < 3; j++)
            {
                Console.WriteLine("Please give Number");
                Age[j] = Convert.ToInt32(Console.ReadLine());
            }
            for (int i = 0; i < Age.Length; i++)
            {
                Console.WriteLine(Age[i]);
            }
        }

        public string ReturnString()
        {
            string[] Age = new string[3];
            Age = ["Mahesh"];
            Console.WriteLine(Age);
            return Age[0];
        }
        public string ReturnName()
        {
            Console.WriteLine("Please give your First Name :");
            var firstName = Console.ReadLine();
            Console.WriteLine("Please give your Last Name :");
            var lastName = Console.ReadLine();
            /* Format() Method*/
            string fullName = string.Format("{0} {1}", firstName, lastName);
            return fullName;
        }
        public string JoinMethod()
        {
            int[] numbers = new int[3] { 1, 2, 3 };
            string JoinedString = string.Join(" ", numbers);
            return JoinedString;
        }
    }
}
