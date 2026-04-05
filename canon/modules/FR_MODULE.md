# FR_MODULE — Французское право (надстройка над LEGAL)

**Профиль:** FR_MODULE (активен поверх LEGAL при французских правовых вопросах)  
**Назначение:** Специфика французского права, процессуальных норм, судебной практики

---

## 1. Условия активации

FR_MODULE активируется автоматически когда:
- Тема содержит: Франция, France, French law, droit français, loi française
- Цитируются французские нормативные акты (Code civil, Code du travail, etc.)
- Проект = `guiyon` (по умолчанию французская юрисдикция)
- Пользователь явно указывает французскую юрисдикцию

---

## 2. Основные источники французского права

### Кодексы (Codes)
| Код | Название | Применение |
|-----|----------|------------|
| CC | Code civil | Договоры, собственность, семья |
| CCom | Code de commerce | Компании, торговля |
| CT | Code du travail | Трудовые отношения |
| CP | Code pénal | Уголовное право |
| CPC | Code de procédure civile | Гражданский процесс |
| CMF | Code monétaire et financier | Финансовое регулирование (AMF) |

### Официальные источники
- **Legifrance** (legifrance.gouv.fr) — все действующие нормы
- **Légifrance Jurisprudence** — решения Cour de cassation, CE, CC
- **Journal Officiel** (journal-officiel.gouv.fr) — новые законы и декреты
- **AMF** (amf-france.org) — финансовое регулирование

---

## 3. Иерархия норм французского права

```
Constitution (1958)
    ↓
Bloc de constitutionnalité
    ↓
Traités internationaux (CEDH, UE)
    ↓
Lois organiques
    ↓
Lois ordinaires
    ↓
Ordonnances (art. 38 Const.)
    ↓
Décrets en Conseil d'État
    ↓
Décrets simples
    ↓
Arrêtés (ministériels, préfectoraux)
    ↓
Circulaires (non contraignantes)
```

---

## 4. Ключевые суды

| Суд | Юрисдикция |
|-----|------------|
| Cour de cassation | Высшая инстанция гражданского/уголовного права |
| Conseil d'État | Административные споры |
| Conseil constitutionnel | Конституционность законов |
| Tribunal de commerce | Коммерческие споры |
| Conseil de prud'hommes | Трудовые споры |
| Tribunal judiciaire | Общая гражданская юрисдикция (с 2020) |

---

## 5. Формат цитирования французских норм

```
Art. L[номер]-[статья] [Код]
→ Art. L1221-1 Code du travail

Art. R[номер]-[статья] [Код]   ← декретные нормы (réglementaires)
→ Art. R1234-1 Code du travail

Cass. [palier], [дата], n° [numéro de pourvoi]
→ Cass. soc., 15 janv. 2020, n° 18-14.001

CE, [дата], n° [requête]
→ CE, 30 oct. 2019, n° 428048
```

---

## 6. Специфика для BANXE / EMI

Применимые французские нормы для финтех/EMI:
- **CMF L314-1 и след.** — платёжные услуги (transposition PSD2)
- **CMF L561-1 и след.** — LCB-FT (AML/CFT)
- **Loi n° 2020-1508 (PACTE)** — токены, ICO, PSAN
- **RGPD** (Règlement UE 2016/679) — protection des données
- **Autorité de contrôle:** ACPR (Banque de France)

---

## 7. Статус

**Версия:** stub 1.0  
**Источник:** построен на основе инструкций пользователя  
**Расширение:** при получении FR_MODULE_2.3 — дополнить детальными процессуальными протоколами
