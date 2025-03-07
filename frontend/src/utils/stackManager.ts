// A simple module to maintain and update the stacking order for windows.
let currentZIndex = 1;

export function getNextZIndex(): number {
    // Increment and return a new z-index to ensure the window is on top.
    currentZIndex += 1;
    return currentZIndex;
} 