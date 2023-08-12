import java.util.HashMap;
import java.util.HashSet;
import java.util.function.Function;
import java.util.function.Supplier;


interface ICakeMaker{
    public String makeCake(String extraIngredents, int amount);
}

class Bakery{

    public void doBaking(ICakeMaker caker){
        System.out.println("We made a cake! This one:" + caker.makeCake("suger", 500));
    }
}

class Main {
        public static void TestBakery(){
            
            Bakery bakery = new Bakery();
            // CakeMaker x = new CakeMaker(); // BADDDD, because we cant instantiate an interface
            // sen1 Make CakeMaker as a implementation of an Interface!
            // exmaple of anonymous inner class
            ICakeMaker chocoMaker = new ICakeMaker() {
                // ??? what??? but CakeMaker is abstract! how??
                @Override
                public String makeCake(String extraIngredents, int amount){
                    return "Chocolate cake, no need for extra ingredents";
                }
            }; 
            bakery.doBaking(chocoMaker);

            // sen#2 we can also use lambda instead!
            // if an Interface only has one method, which ICakeMaker does
            // we can use a lambda function in place of that Interface instead!
            // check *THIS* out!
            bakery.doBaking(
                (in, am)-> {
                    return "Generic cake with" + am + "grams of " + in;
                }
            );
        }

    /**
    Supplier       ()    -> x
    Consumer       x     -> ()
    BiConsumer     x, y  -> ()
    Callable       ()    -> x throws ex
    Runnable       ()    -> ()
    Function       x     -> y
    BiFunction     x,y   -> z
    Predicate      x     -> boolean
    UnaryOperator  x1    -> x2
    BinaryOperator x1,x2 -> x3
     */
    public static void print(Object o) {
        System.out.println(o);
    }

    public static double getSensorValueSumInUnit(double val1, double val2, Function<Double, Double> unitConverter) {
        // input val1 val2 in metric
        return unitConverter.apply(val1) + unitConverter.apply(val2);
    }

    public static void fancyPrint(String stuffToPrint, Function<String, String> decoration) {
        System.out.println(decoration.apply(stuffToPrint));
    }

    public static Supplier<Double> getRandomNumberMaker() {
        return () -> {
            return Math.random();
        };
    }

    public static void main(String[] args) {

TestBakery();


        Supplier<Double> rng = getRandomNumberMaker();
        for (int i = 0; i < 10; i++) {
            print(rng.get());
        }

        fancyPrint("HELLO", (stuff) -> {
            return "*********\n" + stuff + "\n*********\n";
        });

        fancyPrint("HELLO", (stuff) -> {
            return "NON RELAted STRING";
        });

        double planeSpeed = 200;
        double ambiantWindSpeed = 10;

        double sumInMach = getSensorValueSumInUnit(planeSpeed, ambiantWindSpeed, (speed) -> {
            return speed / 1000;
        });

        print(sumInMach);



    }
}