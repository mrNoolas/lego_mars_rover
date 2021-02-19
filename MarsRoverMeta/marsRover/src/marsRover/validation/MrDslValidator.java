/*
 * generated by Xtext 2.23.0
 */
package marsRover.validation;

import java.util.HashSet;

import org.eclipse.xtext.validation.Check;

import marsRover.mrDsl.BackwardMove;
import marsRover.mrDsl.ColorCondition;
import marsRover.mrDsl.Condition;
import marsRover.mrDsl.ConditionSeq;
import marsRover.mrDsl.DistanceConditionBackGT;
import marsRover.mrDsl.DistanceConditionBackLT;
import marsRover.mrDsl.DistanceConditionFrontGT;
import marsRover.mrDsl.DistanceConditionFrontLT;
import marsRover.mrDsl.ForwardMove;
import marsRover.mrDsl.LeftMove;
import marsRover.mrDsl.PondCondition;
import marsRover.mrDsl.RightMove;
import marsRover.mrDsl.SafeBackwardMove;
import marsRover.mrDsl.SafeForwardMove;
import marsRover.mrDsl.SafeLeftMove;
import marsRover.mrDsl.SafeRightMove;

/**
 * This class contains custom validation rules. 
 *
 * See https://www.eclipse.org/Xtext/documentation/303_runtime_concepts.html#validation
 */
public class MrDslValidator extends AbstractMrDslValidator {
	
	@Check
	void checkDegreesLeft(LeftMove move) {
		int degrees = move.getDegrees();
		if(degrees <= 0 | degrees > 360) 
			error("Degrees must be between 1 and 360", null);
	}
	
	@Check
	void checkDegreesSafeLeft(SafeLeftMove move) {
		int degrees = move.getDegrees();
		if(degrees <= 0 | degrees > 360) 
			error("Degrees must be between 1 and 360", null);
	}
	
	
	@Check
	void checkDegreesRight(RightMove move) {
		int degrees = move.getDegrees();
		if(degrees <= 0 | degrees > 360)
			error("Degrees must be between 1 and 360", null);
	}
	
	@Check
	void checkDegreesSafeRight(SafeRightMove move) {
		int degrees = move.getDegrees();
		if(degrees <= 0 | degrees > 360)
			error("Degrees must be between 1 and 360", null);
	}
	
	@Check
	void checkRotationsForward(ForwardMove move) {
		float rotations = Float.parseFloat(move.getDistance());
		if(rotations <= 0) 
			error("Rotations must be more than 0", null);
		if(rotations > 100)
			error("Max rotations is 100", null);
	}
	
	@Check
	void checkRotationsSafeForward(SafeForwardMove move) {
		float rotations = Float.parseFloat(move.getDistance());
		if(rotations <= 0) 
			error("Rotations must be more than 0", null);
		if(rotations > 100)
			error("Max rotations is 100", null);
	}

	@Check
	void checkRotationsBackward(BackwardMove move) {
		float rotations = Float.parseFloat(move.getDistance());
		if(rotations <= 0) 
			error("Rotations must be more than 0", null);
		if(rotations > 100)
			error("Max rotations is 100", null);
	}
	
	@Check
	void checkRotationsSafeBackward(SafeBackwardMove move) {
		float rotations = Float.parseFloat(move.getDistance());
		if(rotations <= 0) 
			error("Rotations must be more than 0", null);
		if(rotations > 100)
			error("Max rotations is 100", null);
	}
		
	@Check
	void checkDistanceFrontLT(DistanceConditionFrontLT condition) {
		int distance = condition.getDistance();
		if(distance <= 0) 
			error("Distance must be positive", null);
	}

	@Check
	void checkDistanceFrontGT(DistanceConditionFrontGT condition) {
		int distance = condition.getDistance();
		if(distance <= 0) 
			error("Distance must be positive", null);
	}
	
	@Check
	void checkDistanceBackLT(DistanceConditionBackLT condition) {
		int distance = condition.getDistance();
		if(distance <= 0) 
			error("Distance must be positive", null);
	}
	
	@Check
	void checkDistanceBackGT(DistanceConditionBackGT condition) {
		int distance = condition.getDistance();
		if(distance <= 0) 
			error("Distance must be positive", null);
	}
	
//	@Check
//	void checkTimeCondition(TimeCondition condition) {
//		int seconds = condition.getSeconds();
//		if(seconds <= 0)
//			error("Seconds must be positive", null);
//	}
	
	@Check
	void checkDuplicateColors(ColorCondition cc) {
		var colorList = cc.getColors();
		for(var i = 0; i < colorList.size(); i++) {
			for(var j = i+1; j < colorList.size(); j++) {
				if(colorList.get(i).name().equals(colorList.get(j).name())) {
					error("Double color", null);
				}
			}
		}
	}
	
	@Check
	void checkDuplicateConditions(ConditionSeq cs) {
		var conditions = cs.getConditions();
		for(var i = 0; i < conditions.size(); i++) {
			for(var j = i+1; j < conditions.size(); j++) {
				Condition condI = conditions.get(i);
				Condition condJ = conditions.get(j);
				if(condI.getCond() instanceof ColorCondition & condJ.getCond() instanceof ColorCondition){
					ColorCondition cc1 = (ColorCondition) condI.getCond();
					ColorCondition cc2 = (ColorCondition) condJ.getCond();
					var cc1Colors = cc1.getColors();
					var cc2Colors = cc2.getColors();
					if(new HashSet<>(cc1Colors).equals(new HashSet<>(cc2Colors))){
						error("Duplicate Color condition", null);
					}
				}
				else if (condI.getCond() instanceof PondCondition & condJ.getCond() instanceof PondCondition){
					PondCondition cc1 = (PondCondition) condI.getCond();
					PondCondition cc2 = (PondCondition) condJ.getCond();
					var pc1Color = cc1.getPond();
					var pc2Color = cc2.getPond();
					if(pc1Color.equals(pc2Color)){
						error("Duplicate Pond condition", null);
					}
				}
			}
		}
	}
}
