# /new-screen — Create a new BANXE UI Screen

## Steps

### 1. Identify the screen in the inventory
Read `~/banxe-architecture/docs/BANXE-SCREEN-INVENTORY.md`.
Find the target screen entry by ID (W-01..W-06 for web, M-01..M-06 for mobile).
Note: required components, data, states, accessibility requirements.

### 2. Check what components already exist
```bash
cat ~/banxe-ui/packages/ui/src/index.ts
ls ~/banxe-ui/packages/ui/src/financial/
```
Never invent a component that already exists. Never invent a Tailwind class not in the design system.

### 3. Write the screen spec as a header comment
Every screen file opens with a spec comment:
```tsx
/**
 * ScreenName — W-XX / M-XX
 *
 * Purpose: ...
 * Required components: ...
 * Data: ...
 * States: loading | loaded | error | empty
 * Accessibility: ...
 */
```

### 4. Create the screen file
- **Web:** `~/banxe-ui/apps/web/src/screens/<Name>/index.tsx`
- **Mobile:** `~/banxe-ui/apps/mobile/src/screens/<Name>.tsx`

Follow existing patterns from Dashboard screen:
```bash
cat ~/banxe-ui/apps/web/src/screens/Dashboard/index.tsx
```

Rules:
- All amounts → monospace font (`font-mono`)
- Loading state → skeleton divs, never spinner-only
- Error state → inline error message + retry button
- Empty state → descriptive message + primary CTA
- ARIA labels on all interactive elements
- AI content → always has `--color-ai-accent` badge + confidence

### 5. Update the screen index (if it exists)
```bash
# Check for barrel export:
cat ~/banxe-ui/apps/web/src/screens/index.ts 2>/dev/null
```
Add: `export { ScreenName } from './<ScreenName>'`

### 6. Write unit test
- **Web:** `~/banxe-ui/tests/unit/<name>.test.tsx`
- **Mobile:** `~/banxe-ui/tests/unit/<name>.mobile.test.tsx`

Test:
- Renders without crashing
- Loading skeleton shown (mock data loading)
- Data rendered correctly
- Error state shown on fetch failure
- Key ARIA labels present

### 7. Write accessibility test
`~/banxe-ui/tests/a11y/<name>.a11y.test.tsx` — run axe-core:
```tsx
import { axe } from 'jest-axe'
const results = await axe(container)
expect(results).toHaveNoViolations()
```

### 8. Run quality checks
```bash
cd ~/banxe-ui
npm run typecheck
npm run lint
npm test
```

### 9. Commit
```bash
cd ~/banxe-ui && git add -A && git commit -m "feat(screens): add <ScreenName> screen (W-XX / M-XX)"
```

---

## Design System Quick Reference

| Token | Usage |
|-------|-------|
| `bg-bg-base` | Page background |
| `bg-surface` | Card / panel |
| `bg-elevated` | Modal, dropdown |
| `text-primary` | Headings, content |
| `text-secondary` | Labels, captions |
| `text-brand-primary` | Links, CTAs |
| `font-mono` | Amounts, IBANs, references |
| `text-success` | Received, confirmed |
| `text-warning` | Pending, review |
| `text-error` | Failed, blocked |
| `text-ai-accent` | AI-generated content marker |

## Component Import Pattern
```tsx
import {
  BalanceWidget,
  TransactionRow,
  StatusChip,
  AmountInput,
  AIInsightCard,
  ComplianceFlag,
} from '@banxe/ui'
import type { TransactionStatus, ChipStatus } from '@banxe/ui'
```
