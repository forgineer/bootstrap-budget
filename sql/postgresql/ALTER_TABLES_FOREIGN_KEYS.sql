/**
 * Name: ALTER_TABLES_FOREIGN_KEYS.sql
 * Purpose: Alters all Bootstrap Budget tables with FOREIGN KEYs
 * Author: Blake Phillips (forgineer)
 */
ALTER TABLE public.config ADD CONSTRAINT config_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.account ADD CONSTRAINT account_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
ALTER TABLE public.account ADD CONSTRAINT account_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.budget ADD CONSTRAINT budget_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.user_budget ADD CONSTRAINT user_budget_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
ALTER TABLE public.user_budget ADD CONSTRAINT user_budget_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public."transaction" ADD CONSTRAINT transaction_fk FOREIGN KEY (account_id) REFERENCES public.account(account_id);
ALTER TABLE public."transaction" ADD CONSTRAINT transaction_fk_1 FOREIGN KEY (budget_item_id) REFERENCES public.budget_item(budget_item_id);
ALTER TABLE public."transaction" ADD CONSTRAINT transaction_fk_2 FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.dashboard ADD CONSTRAINT dashboard_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
ALTER TABLE public.dashboard ADD CONSTRAINT dashboard_fk_1 FOREIGN KEY (budget_item_id) REFERENCES public.budget_item(budget_item_id);

ALTER TABLE public.budget_item ADD CONSTRAINT budget_item_fk FOREIGN KEY (budget_id) REFERENCES public.budget(budget_id);
ALTER TABLE public.budget_item ADD CONSTRAINT budget_item_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(user_id);
