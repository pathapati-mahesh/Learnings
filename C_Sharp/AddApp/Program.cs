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

        static string returnDetails()
        {
            string name;
            name = "Mahesh";
            //city = "Frankfurt";
            //nationality = "Indian";
            //state = "Hesse";
            //profession = "Student";
            return name;
            //Console.WriteLine($"Name :{name}, Nationality :{nationality}, City :{city}, state :{state}, Profession :{profession}");
        }
        static int implicitConversion()
        {
            /*
            In Implicit conversion we are not going to take care of converting the type of data. It will be done by the compiler
            while building the application itself. This is so called implicit conversion.
            */
            byte number = 1;
            int num = number;
            return num;
        }

        static bool convertIncompTypebool(int value)
        {
            /*
              Conversion betweeen Non Compatable Types it will be done by using a Module called as "convert"

             */
            bool expression=Convert.ToBoolean(value);
            return expression;
        }
        static int convertIncompTypeint(string Code)
        {
            int ConvCode = Convert.ToInt32(Code);
            return ConvCode;
        }
        static int explicitConversion()
        {
            /*
            Incase of Explicit conversion we have the data loss as we are forecefully converting the datatype of the value
            from one to the another.
            Syntax : (data Type) 'variable/value that we are trying to convert'
            Note:
                In this case sometimes the dataloss chances are there But not in All cases. If we have the data/value that we are storing
                in within the range of the value
            """*/
            int num = 400;
            byte number = (byte)num;
            return number;
        }

        static void Main(String[] args)
        {
            Console.WriteLine($"Adding Two Numbers :{2 + 3}");
            int value=overflow();
            Console.WriteLine($"Over flow Value is :{value}");
            string name=returnDetails();
            Console.WriteLine($"Name :{name}");
            int implicitConv = implicitConversion();
            Console.WriteLine($"Implicit Conversion :{implicitConv}");
            int explicitConv = explicitConversion();
            Console.WriteLine($"Explicit Conversion :{explicitConv}");
            Console.WriteLine($"Converting Incompatable Type string value to Boolean Value :{convertIncompTypebool(1)}");
            Console.WriteLine($"Converting Incompatable Type string value to int Value :{convertIncompTypeint("909090")}");
        }
    }
}