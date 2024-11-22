namespace ClassAndStruct
{
    struct Employee
    {
        public string Name;
    }
    public class StructProgram
    {
        public void EmpInformation()
        {
            Employee emp1 = new Employee();
            emp1.Name = "Maheshuuuuuuuuuuu";
            Employee emp2 = emp1;
            emp2.Name = "Mohithhhhhhhhhhhhhh";
            Console.WriteLine($"Employee Name One :{emp1.Name} & Employee Name Two :{emp2.Name}");

        }

    }
}
