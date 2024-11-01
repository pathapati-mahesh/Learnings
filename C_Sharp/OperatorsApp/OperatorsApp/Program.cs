using ChildOperatorsFile;


namespace OperatorsApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Methods methods = new Methods();
            Console.WriteLine($"Addition of Two Numbers :{ methods.AddFunc(2,3)}");
            Console.WriteLine($"Substraction of Two Numbers :{methods.SubstractFunc(2, 3)}");
            Console.WriteLine($"Multiplication of Two Numbers :{methods.MultiplyFunc(2, 3)}");
            Console.WriteLine($"Division of Two Numbers :{methods.DivideFunc(3, 2)}");
            Console.WriteLine($"Remainder of Two Numbers :{methods.RemaindeFunc(3, 2)}");
            Console.WriteLine($"Increment of Two Numbers (Preincrement & Post Increment) :{methods.IncrementFunc(2, 1)}");
            Console.WriteLine($"Increment of Two Numbers (Pre Decrement & Post Decrement) :{methods.DecrementFunc(2, 1)}");
        }
    }
}
