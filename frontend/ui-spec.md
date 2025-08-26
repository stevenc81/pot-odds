# Pot Odds Calculator Frontend Specification

## Overview

Design a modern, user-friendly frontend for the Pot Odds Calculator that allows poker players to easily select cards, view real-time pot odds calculations, and access advanced outs analysis. The interface must be highly responsive, work seamlessly on both desktop and mobile, and offer interactive features that cater to casual users and poker experts alike.

***

## UI/UX Requirements

### 1. Dark Theme Toggle

- **Feature:** A toggle switch lets users switch between Light and Dark themes instantly.
- **Placement:** Fixed at the top-right corner of the page, always accessible regardless of screen size.
- **Implementation:** Theme preference is stored locally (e.g., in localStorage), and persists on next load.  
- **Styling:** True dark mode with high contrast, softer background, and accented color highlights for selected cards or outs.

***

### 2. Card Selection Interface

#### A. Hole Card Selection Area

- **Purpose:** Let users choose exactly two "hole cards" (private cards).
- **Design:**
  - *Card Grid*: Display all 52 cards in a clear, touch-friendly grid.
  - *Selection Rule*: Enforce selection of exactly two cards, never duplicates.
  - *Feedback*: Visually highlight selected cards (with color border, glow, or animation).
  - *Accessibility*: Large clickable/tappable hitboxes for easy selection.
  - *Labels*: Area labeled "Hole Cards" with a persistent count indicator ("2 of 2 selected").

#### B. Community Card Selection Area

- **Purpose:** Allow users to pick up to five community cards.
- **Design:**
  - *Card Grid*: Same as above but may be visually separated or stacked below.
  - *Selection Rule*: Allow 0-5 cards, enforce no duplicates with hole cards.
  - *Feedback*: Highlight selected community cards distinctly from hole cards.
  - *Labels*: Area labeled "Community Cards" with count indicator ("0-5 selected").

#### C. Interactivity

- **Mouse & Touch Support:** Card selection and deselection must work equally well with mouse clicks or finger taps (optimized for mobile).
- **Adaptive Hitboxes:** Card hitboxes scale automatically with screen size for mobile usability.
- **Invalid Input Handling:** Prevent users from selecting more than allowed cards or duplicate cards. Display contextual error messages as needed.

***

### 3. Real-time Calculation Updates

- **Live Feedback:** Every time the card selection changes (via selection or deselection), automatically trigger a calculation API call to `/api/calculate`.
- **Loading State:** Show a spinner or loading animation during API call to indicate pending calculation.
- **Result Display:**  
  - Show latest pot odds ratio (large, prominent font).
  - List all identified outs, grouped and color-coded by draw type (flush, straight, pair, etc.).
  - Responsive layout: Results adapt layout fluidly from stacked (mobile) to side-by-side (desktop).
  - Error Handling: If calculation fails (e.g., validation error), show the API error message to the user.

***

### 4. Reset Button

- **Function:** Clears all selected cards instantly (both hole and community areas).
- **Placement:** Prominently placed below card selection interface.
- **UI/UX:** Button uses a distinctive color (e.g., red or accent) and confirmation animation.
- **Effect:** After reset, results area is cleared and API is not called until a valid selection is made.

***

### 5. Responsive & Adaptive Design

- **Layout Adaptivity:** UI seamlessly rearranges for wide desktop screens or narrow mobile screens.
  - On desktop: Arrange hole and community panels side-by-side; display outs analysis next to results.
  - On mobile: Stack panels vertically; condense controls and use collapsible sections for outs.
- **Touch Hotspots:** Card selections and reset are optimized for finger tapping on phones/tablets.
- **Font & Element Scaling:** All fonts, hitboxes, cards, buttons scale to ensure legibility and usability on all device types.

***

### 6. Clean & Elegant Design

- **Minimal Text:** Avoid excessive description text that clutters the UI. Use concise, essential labels only.
- **Visual Hierarchy:** Prioritize visual elements over text explanations. Let the interface be self-explanatory through design.
- **Whitespace:** Use generous whitespace to create breathing room and improve readability.
- **Icon Usage:** Prefer intuitive icons over text where possible (e.g., reset icon, theme toggle icon).
- **Progressive Disclosure:** Hide advanced features or detailed explanations behind expandable sections or tooltips.

### 7. Accessibility & Usability

- **Keyboard Navigation:** All controls (cards, reset button, theme toggle) accessible via tab and keyboard.
- **Screen Reader Support:** Aria labels and role attributes for interactive elements, especially card selections.
- **Contrast Compliance:** Ensure WCAG-compliant contrast for visual elements in both light and dark modes.
- **Error Recovery:** Friendly, actionable error messages for invalid selections, calculation failures, or connectivity issues.

***

## API Integration Logic

- **Endpoint:** `POST /api/calculate`
- **Payload:**  
  ```
  {
    "hole_cards": ["As", "Kh"],
    "community_cards": ["Qs", "Jd", "Tc"]
  }
  ```
- **On Selection Change:**  
  - Validate current card selections.
  - If valid (2 hole, 0-5 unique community, no duplicates), send API request.
  - On response: Show pot odds ratio, outs list, group and color-code outs by draw type.
  - On error: Show contextual message (invalid card, duplicates, etc.).

***

## Summary Table of Components

| Component            | Description                                        | Key Features                         |
|----------------------|----------------------------------------------------|--------------------------------------|
| Theme Toggle         | Switch between dark/light mode                     | Persistent, accessible, instant      |
| Hole Card Area       | Select exactly 2 private cards                     | No duplicates, touch/mouse input     |
| Community Area       | Add up to 5 community cards                        | No duplicates, adaptive grid         |
| Results Panel        | Shows pot odds ratio & outs analysis               | Responsive, real-time update         |
| Reset Button         | Clears selections                                  | One-tap, prominent, animated         |
| Adaptive Layout      | Desktop/mobile optimization                        | Touch-friendly, font scaling         |
| Accessibility        | Keyboard, screen reader, error handling            | ARIA labels, contrast, feedback      |

***

## Example User Flow

1. User opens app on phone or desktop.
2. Selects two hole cards ("As", "Kh") by clicking/tapping.
3. Selects three community cards ("Qs", "Jd", "Tc").
4. API is called; pot odds and outs are displayed instantly.
5. User toggles dark mode for better visibility.
6. User wants to test a new scenario, taps "Reset", all selections clear.
7. Repeats card selection; instant feedback loop.

