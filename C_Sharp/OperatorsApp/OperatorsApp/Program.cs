using ChildOperatorsFile;
using ClassAndStruct;
using ArraysExamples;


namespace OperatorsApp
{
    struct Employee
    {
        public int Id;
        public string Name;
        public string Profession;

        internal class Program
        {
            static void Main(string[] args)
            {
                Methods methods = new Methods();
                Console.WriteLine($"Addition of Two Numbers :{methods.AddFunc(2, 3)}");
                Console.WriteLine($"Substraction of Two Numbers :{methods.SubstractFunc(2, 3)}");
                Console.WriteLine($"Multiplication of Two Numbers :{methods.MultiplyFunc(2, 3)}");
                Console.WriteLine($"Division of Two Numbers :{methods.DivideFunc(3, 2)}");
                Console.WriteLine($"Remainder of Two Numbers :{methods.RemaindeFunc(3, 2)}");
                Console.WriteLine($"Increment of Two Numbers (Preincrement & Post Increment) :{methods.IncrementFunc(2, 1)}");
                Console.WriteLine($"Increment of Two Numbers (Pre Decrement & Post Decrement) :{methods.DecrementFunc(2, 1)}");

                Console.WriteLine("---------------------------------------Classes_Structs---------------------------------------------------");

                Console.WriteLine($"Accessing the static Method Directly using the class Name with out creating the object");
                Console.WriteLine($"Even if we create we cannot be able to access the static methods declared inside the class");
                Console.WriteLine($"Accessing the static Method Directly using the class Name with out creating the object");
                Console.WriteLine(Methods.converter(2, 3));
                Employee emp1 = new Employee();
                emp1.Name = "Mahesh";
                Employee emp2 = emp1;
                emp2.Name = "Manoj";
                Console.WriteLine($"Employee Name One :{emp1.Name} & Employee Name Two :{emp2.Name}");
                StructProgram classCreated = new StructProgram();
                classCreated.EmpInformation();
                Console.WriteLine("------------------------------------Arrays----------------------------------------");
                ArraySession arraysExamples = new ArraySession();
                int age = arraysExamples.LearnArrays();
                Console.WriteLine(age);
                arraysExamples.RotateArray();
                Console.WriteLine(arraysExamples.ReturnString());
                Console.WriteLine("------------------------------------Strings---------------------------------------");
                Console.WriteLine(arraysExamples.ReturnName());

                Console.WriteLine(arraysExamples.JoinMethod());



            }
        }
    }
}
