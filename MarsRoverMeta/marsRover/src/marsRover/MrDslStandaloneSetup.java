/*
 * generated by Xtext 2.23.0
 */
package marsRover;


/**
 * Initialization support for running Xtext languages without Equinox extension registry.
 */
public class MrDslStandaloneSetup extends MrDslStandaloneSetupGenerated {

	public static void doSetup() {
		new MrDslStandaloneSetup().createInjectorAndDoEMFRegistration();
	}
}