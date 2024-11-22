using System;
namespace InfoClass {
	public static class PractiseClass
	{
		public static string Excercise(string Name, int Experience, string Profession)
		{
			string Message = $"Hello This is {Name}. Im working as a {Profession} from last {Experience} years."
			return Message;
		}
	}
}
