import java.util.Scanner;

public class Classes 
{
    public static void main(String[] args)
    {
        String answer = new String();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a fully qualified class name: ");
        answer = scanner.nextLine();
        System.out.println(answer);

        scanner.close();
    }
    public static void printSuperclasses(Object o)
    {
        Class subclass = o.getClass();
        Class superclass = subclass.getSuperclass();

        while (superclass != null)
        {
            String className = superclass.getName();
            System.out.println(className);
            subclass = superclass;
            superclass = subclass.getSuperclass();
        }
    }    
}
