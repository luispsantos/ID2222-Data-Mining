package se.kth.jabeja.config;

/**
 * Select the simulated annealing policy (standard, exponential, improved exponential).
 */
public enum AnnealingSelectionPolicy {
    LINEAR("LINEAR"),
    EXPONENTIAL("EXPONENTIAL"),
    IMPROVED_EXP("IMPROVED_EXP");

    String name;

    AnnealingSelectionPolicy(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return name;
    }
}
