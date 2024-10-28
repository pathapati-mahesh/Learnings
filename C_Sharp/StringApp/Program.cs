using System;

class convertString
{
    static string convertName(string name,string profession)
    {
        if (name == null){
            return "Name should not be Null";
        }
        if (profession == null) {
            return "Profession Should Not be Null";
        }            
        if (name.Contains("Ma")){
            return "Name has the Character Ma";
        }
        if (profession=="Software Developer")
        {
            return "Hip Hip Hurray. Its My Fav Profession";
        }
        else
        {
            return (name + " " + profession);
        }
    }
    static void Main(string[] args)
    {
        Console.WriteLine("Result of the Application");
        string dev_name = Console.ReadLine();
        string Profession = Console.ReadLine();
        if ((dev_name!=null) || (Profession!=null) )
        {
            string callFunc = convertName(dev_name, Profession);
            Console.WriteLine(callFunc);
        }
        else
        {
            Console.WriteLine($"Please give the Input {dev_name},{Profession}");
        }
    }
}