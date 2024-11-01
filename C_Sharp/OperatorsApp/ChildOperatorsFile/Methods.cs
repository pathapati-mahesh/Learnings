namespace ChildOperatorsFile
{
    public class Methods
    {
        public int AddFunc(int a, int b)
        {
            return a + b;
        }
        public int SubstractFunc(int a, int b)
        {
            return a - b;
        }
        public int MultiplyFunc(int a, int b)
        {
            return a * b;
        }
        public int DivideFunc(int a, int b)
        {
            return a / b;
        }
        public int RemaindeFunc(int a, int b)
        {
            return a % b;
        }
        public int IncrementFunc(int a, int b)
        {
            int PostIncrementOpp = (a++) + (b++);
            int PreIncrementOpp = (++a) + (++b);
            int SumOfBoth =PreIncrementOpp + PostIncrementOpp;
            return SumOfBoth;

        }
        public int DecrementFunc(int a, int b) {
            int PostDecrementOpp = (a--) + (b--);
            int PreDecrementOpp = (--a) + (--b);
            int SumOfBoth = PreDecrementOpp + PostDecrementOpp;
            return SumOfBoth;
        }
    }
}
