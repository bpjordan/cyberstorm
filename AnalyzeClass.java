import java.lang.reflect.*;

public class AnalyzeClass
{

    public static void main(String[] args)
    {

        try
        {
            Class c = Class.forName(args[0]);
            Object o = c.newInstance();
            System.out.println("Class: " + c.toString());

            Constructor constructors[] = c.getDeclaredConstructors();
            System.out.println("Constructors:");
            for(Constructor s: constructors)
                System.out.println("\t" + s.toString());

            Method methods[] = c.getDeclaredMethods();
            System.out.println("Methods:");
            for(Method m: methods)
                System.out.println("\t" + m.toString());



            Field fields[] = c.getDeclaredFields();
            System.out.println("Fields:");
            for(Field f: fields)
            {
                System.out.print("\t" + f.toString());
                try
                {
                    f.setAccessible(true);
                    System.out.println(" (Val:" + f.get(o) + ")");
                }
                catch (Throwable e)
                {
                    System.out.println();
                }
            }


        }
        catch (Throwable e)
        {
            System.err.println(e);
        }

    }

}

