# Agent rules (frontend)

- New and refactored UI uses Shadcn UI (`@/components/ui/*`) and Tailwind CSS. Do NOT use Material UI (MUI) in new code; legacy MUI screens are being migrated gradually.
- Never use `any` in TypeScript.
- All user-facing text goes through `t('...')` from react-i18next. Add every new key to both `frontend/src/locales/vi/*.json` and `frontend/src/locales/en/*.json`.
- Buttons, badges and tags use micro radius (`rounded-sm`, `rounded-[3px]`), never pills (`rounded-full`, `rounded-xl`).
- Never use the em dash character in UI text or docs.
