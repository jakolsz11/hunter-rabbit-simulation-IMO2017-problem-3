import matplotlib.pyplot as plt
import numpy as np
import mpmath as mp
from hunter_rabbit_modified_assumptions_hp import simulate as simulate_modified
from hunter_rabbit_original_rules_hp import simulate as simulate_original
from config import A


def get_data(a=2.0):
    """
    Get simulation data for both modified and original.
    """
    print("Starting simulation for modified...")
    data_modified = simulate_modified(a=a, D_limit=mp.mpf('100.0'))
    print("Modified simulation completed.")
    print("Starting simulation for original...")
    data_original = simulate_original(a=mp.mpf(str(a)), D_limit=mp.mpf('100.0'))
    print("Original simulation completed.")

    return {
        "modified": data_modified,
        "original": data_original,
        "a": a,
    }


def draw_plots(data):

    D_modified = np.array([float(x) for x in data["modified"]["D"]])
    D_original = np.array([float(x) for x in data["original"]["D"]])

    fig, ax_D = plt.subplots(1, 1, figsize=(12, 8))

    ax_D.plot(D_modified, color="green", label='D in Modified Simulation', lw=0.7)
    ax_D.plot(D_original, color="orange", label='D in Original Simulation', lw=0.7)
    ax_D.axvline(len(D_modified)-1, color="green", linestyle="--", alpha=0.5)
    ax_D.text(len(D_modified)+100, D_modified[-1]+1, f'Modified end ({len(D_modified)-1})', color="green", ha="left", va="bottom")
    ax_D.axvline(len(D_original)-1, color="orange", linestyle="--", alpha=0.5)
    ax_D.text(len(D_original)-100, D_original[-1]+1, f'Original end ({len(D_original)-1})', ha="right", va="bottom", color="orange")
    ax_D.set_xlabel('Cycle')
    ax_D.set_ylabel('Distance between hunter and rabbit', fontsize=12)
    ax_D.ticklabel_format(axis='x', style='plain')
    ax_D.grid()
    ax_D.set_title(f'Distance between hunter and rabbit in modified and original simulations for a={data["a"]}')
    ax_D.legend()

    plt.show()


if __name__ == "__main__":
    data = get_data(a=A)
    draw_plots(data)