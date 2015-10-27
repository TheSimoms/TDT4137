import java.util.*;


public class MamdaniFuzzyReasoner {
    private static double triangle(double pos, double x0, double x1, double x2, double clip){
        double value = 0.0;

        if(pos >= x0 && pos <= x1){
            value = (pos - x0) / (x1 - x0);
        }else if(pos >= x1 && pos <= x2){
            value = (x2 - pos) / (x1 - x0);
        }

        if(value > clip){
            value = clip;
        }

        return value;
    }

    private static double grade(double pos, double x0, double x1, double clip){
        double value;

        if(pos >= x1){
            value = 1.0;
        }else if(pos <= x0){
            value = 0.0;
        }else{
            value = (pos - x0) / (x1 - x0);
        }

        if(value > clip){
            value = clip;
        }

        return value;
    }

    private static double reverseGrade(double pos, double x0, double x1, double clip){
        double value;

        if(pos >= x1){
            value = 0.0;
        }else if(pos <= x0){
            value = 1.0;
        }else{
            value = (x1 - pos) / (x1 - x0);
        }

        if(value > clip){
            value = clip;
        }

        return value;
    }

    private static double and(double value1, double value2){
        return Math.min(value1, value2);
    }

    private static double or(double value1, double value2){
        return Math.max(value1, value2);
    }

    private static double not(double value){
        return 1.0 - value;
    }

    private static double findCenterOfGravity(double none, double slowDown, double speedUp,
                                       double floorIt, double brakeHard){
        double max;

        double numerator = 0.0;
        double denominator = 0.0;

        for(double i=-10.0; i<=10.0; i+=0.1){
            List<Double> values = Arrays.asList(
                reverseGrade(i, -8.0, -5.0, brakeHard), triangle(i, -7.0, -4.0, -1.0, slowDown),
                triangle(i, -3.0, 0.0, 3.0, none), triangle(i, 1.0, 4.0, 7.0, speedUp), grade(i, 5.0, 8.0, floorIt)
            );

            max = Collections.max(values);

            numerator += max * i;
            denominator += max;
        }

        return numerator / denominator;
    }

    public static Map<String, Double> run_reasoner(double distance, double delta){
        double distanceVerySmall = reverseGrade(distance, 1.0, 2.5, 1.0);
        double distanceSmall = triangle(distance, 1.5, 3.0, 4.5, 1.0);
        double distancePerfect = triangle(distance, 3.5, 5.0, 6.5, 1.0);
        double distanceBig = triangle(distance, 5.5, 7.0, 8.5, 1.0);
        double distanceVeryBig = grade(distance, 7.5, 9.0, 1.0);

        double deltaShrinkingFast = reverseGrade(delta, -4.0, -2.5, 1.0);
        double deltaShrinking = triangle(delta, -3.5, -2.0, -0.5, 1.0);
        double deltaStable = triangle(delta, -1.5, 0.0, 1.5, 1.0);
        double deltaGrowing = triangle(delta, 0.5, 2.0, 3.5, 1.0);
        double deltaGrowingFast = grade(delta, 2.5, 4.0, 1.0);

        double actionNone = and(distanceSmall, deltaGrowing);
        double actionSlowDown = and(distanceSmall, deltaStable);
        double actionSpeedUp = and(distancePerfect, deltaGrowing);
        double actionFloorIt = and(distanceVeryBig, or(not(deltaGrowing), not(deltaGrowingFast)));
        double actionBrakeHard = distanceSmall;

        double centerOfGravity = findCenterOfGravity(actionNone, actionSlowDown, actionSpeedUp,
                actionFloorIt, actionBrakeHard);

        double brakeHard = reverseGrade(centerOfGravity, -8.0, -5.0, actionBrakeHard);
        double slowDown = triangle(centerOfGravity, -7.0, -4.0, -1.0, actionSlowDown);
        double none = triangle(centerOfGravity, -3.0, 0.0, 3.0, actionNone);
        double speedUp = triangle(centerOfGravity, 1.0, 4.0, 7.0, actionSpeedUp);
        double floorIt = grade(centerOfGravity, 5.0, 8.0, actionFloorIt);

        String actionName = "BrakeHard";
        double actionValue = brakeHard;

        if(slowDown > actionValue){
            actionName = "SlowDown";
            actionValue = slowDown;
        }

        if(none > actionValue){
            actionName = "None";
            actionValue = none;
        }

        if(speedUp > actionValue){
            actionName = "SpeedUp";
            actionValue = speedUp;
        }

        if(floorIt > actionValue){
            actionName = "FloorIt";
            actionValue = floorIt;
        }

        Map<String, Double> result = new HashMap<>();

        result.put(actionName, actionValue);

        return result;
    }

    public static void main(String[] args){
        Map<String, Double> result = run_reasoner(3.70, 1.0);

        System.out.println(result);
    }
}
