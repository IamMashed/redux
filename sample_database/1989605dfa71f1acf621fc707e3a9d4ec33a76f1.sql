--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: assessment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assessment (
    id integer NOT NULL,
    apn character varying,
    county character varying,
    value double precision,
    assessment_date date,
    assessment_type character varying
);


--
-- Name: assessment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.assessment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: assessment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.assessment_id_seq OWNED BY public.assessment.id;


--
-- Name: assessment_validation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assessment_validation (
    id integer NOT NULL,
    apn character varying,
    county character varying,
    errors json
);


--
-- Name: assessment_validation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.assessment_validation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: assessment_validation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.assessment_validation_id_seq OWNED BY public.assessment_validation.id;


--
-- Name: inventory_rules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventory_rules (
    id integer NOT NULL,
    full_bath integer,
    half_bath integer,
    gla_sqft integer,
    lot_sqft integer,
    garage integer,
    basement_prices integer[],
    price_end integer,
    price_start integer
);


--
-- Name: inventory_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inventory_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inventory_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inventory_rules_id_seq OWNED BY public.inventory_rules.id;


--
-- Name: property; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.property (
    id integer NOT NULL,
    apn character varying NOT NULL,
    county character varying NOT NULL,
    school_district integer,
    section character varying,
    block character varying,
    undefined_field character varying,
    lot character varying,
    address character varying,
    street character varying,
    number character varying,
    state character varying,
    latitude double precision,
    longitude double precision,
    property_class integer,
    sale_contract_date date,
    sale_price integer,
    age integer,
    gla_sqft double precision,
    waterfront boolean,
    property_style character varying(255),
    garage integer,
    basement_code character varying(255),
    price_per_sqft double precision,
    lot_size double precision,
    location character varying(255),
    full_baths double precision,
    half_baths double precision,
    hamlet character varying,
    is_condo boolean,
    is_listed boolean,
    kitchens integer,
    town character varying NOT NULL,
    zip integer
);


--
-- Name: property_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.property_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: property_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.property_id_seq OWNED BY public.property.id;


--
-- Name: property_validation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.property_validation (
    id integer NOT NULL,
    apn character varying,
    county character varying,
    errors json
);


--
-- Name: property_validation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.property_validation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: property_validation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.property_validation_id_seq OWNED BY public.property_validation.id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role (
    id integer NOT NULL,
    name character varying(80),
    description character varying(255)
);


--
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;


--
-- Name: roles_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles_users (
    user_id integer,
    role_id integer
);


--
-- Name: ruleset; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ruleset (
    id integer NOT NULL,
    county character varying NOT NULL,
    township character varying NOT NULL,
    proximity integer,
    price_from integer,
    price_to integer,
    date_from date,
    date_to date,
    same_class boolean,
    same_style boolean,
    same_street boolean
);


--
-- Name: ruleset_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ruleset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ruleset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ruleset_id_seq OWNED BY public.ruleset.id;


--
-- Name: selection_rules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.selection_rules (
    id integer NOT NULL,
    proximity_range numeric(10,3)
);


--
-- Name: selection_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.selection_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: selection_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.selection_rules_id_seq OWNED BY public.selection_rules.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255),
    username character varying(50),
    password character varying(255),
    active boolean,
    confirmed_at timestamp without time zone
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: assessment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment ALTER COLUMN id SET DEFAULT nextval('public.assessment_id_seq'::regclass);


--
-- Name: assessment_validation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_validation ALTER COLUMN id SET DEFAULT nextval('public.assessment_validation_id_seq'::regclass);


--
-- Name: inventory_rules id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_rules ALTER COLUMN id SET DEFAULT nextval('public.inventory_rules_id_seq'::regclass);


--
-- Name: property id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.property ALTER COLUMN id SET DEFAULT nextval('public.property_id_seq'::regclass);


--
-- Name: property_validation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.property_validation ALTER COLUMN id SET DEFAULT nextval('public.property_validation_id_seq'::regclass);


--
-- Name: role id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);


--
-- Name: ruleset id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ruleset ALTER COLUMN id SET DEFAULT nextval('public.ruleset_id_seq'::regclass);


--
-- Name: selection_rules id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.selection_rules ALTER COLUMN id SET DEFAULT nextval('public.selection_rules_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
a3235a3643da
\.


--
-- Data for Name: assessment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.assessment (id, apn, county, value, assessment_date, assessment_type) FROM stdin;
1	34  E  00010	nassau	586	2019-12-15	final
2	34  E  00020	nassau	627	2019-12-15	final
3	34  E  00030	nassau	669	2019-12-15	final
4	34  E  00040	nassau	374	2019-12-15	final
5	34  E  00050	nassau	510	2019-12-15	final
6	34  E  00060	nassau	577	2019-12-15	final
7	34  E  00070	nassau	586	2019-12-15	final
8	34  E  00080	nassau	792	2019-12-15	final
9	34  E  00630	nassau	477	2019-12-15	final
10	34  E  00660	nassau	408	2019-12-15	final
11	34  E  00690	nassau	333	2019-12-15	final
12	34  E  00720	nassau	298	2019-12-15	final
14	34  E  00750	nassau	822	2019-12-15	final
15	34  E  00800	nassau	538	2019-12-15	final
16	34  E  00830	nassau	659	2019-12-15	final
\.


--
-- Data for Name: assessment_validation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.assessment_validation (id, apn, county, errors) FROM stdin;
\.


--
-- Data for Name: inventory_rules; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.inventory_rules (id, full_bath, half_bath, gla_sqft, lot_sqft, garage, basement_prices, price_end, price_start) FROM stdin;
1	12000	5000	70	4	6000	{0,7500,15000,22500,30000}	900000	300000
\.


--
-- Data for Name: property; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.property (id, apn, county, school_district, section, block, undefined_field, lot, address, street, number, state, latitude, longitude, property_class, sale_contract_date, sale_price, age, gla_sqft, waterfront, property_style, garage, basement_code, price_per_sqft, lot_size, location, full_baths, half_baths, hamlet, is_condo, is_listed, kitchens, town, zip) FROM stdin;
1	34  E  00010	nassau	1	34	E	  	10	27  HEDGEWAY CT	HEDGEWAY	27 	NY	1091969	199515	2100	2019-12-15	734562	1948	1896	f		\N	4	\N	0.261699999999999988		1	1	\N	\N	\N	\N	1	\N
2	34  E  00020	nassau	1	34	E	  	20	4  SARATOGA CIR	SARATOGA	4 	NY	1092046	199590	2100	2019-12-15	597778	1997	1244	f	1	\N	0	\N	0.178400000000000003		2	0	\N	f	\N	\N	1	\N
3	34  E  00030	nassau	1	34	E	  	30	6  SARATOGA CIR	SARATOGA	6 	NY	1091986	199663	2100	2019-12-15	646726	1926	1365	f	1	\N	4	\N	0.185599999999999987		1	0	\N	f	\N	\N	1	\N
4	34  E  00040	nassau	1	34	E	  	40	8  SARATOGA CIR	SARATOGA	8 	NY	1091928	199696	2100	2019-12-15	530182	1954	1370	f	1	\N	4	\N	0.162000000000000005		1	0	\N	f	\N	\N	1	\N
5	34  E  00050	nassau	1	34	E	  	50	2  LEXINGTON CIR	LEXINGTON	2 	NY	1091883	199758	2100	2019-12-15	566183	1937	1488	f	1	\N	4	\N	0.183700000000000002		1	1	\N	f	\N	\N	1	\N
6	34  E  00060	nassau	1	34	E	  	60	4  LEXINGTON CIR	LEXINGTON	4 	NY	1091948	199825	2100	2019-12-15	611990	1927	2118	f	1	\N	4	\N	0.148499999999999993	20	3	0	\N	f	\N	\N	1	\N
7	34  E  00070	nassau	1	34	E	  	70	6  LEXINGTON CIR	LEXINGTON	6 	NY	1091917	199913	2100	2019-12-15	701546	1926	2968	f	1	\N	4	\N	0.154299999999999993	20	6	0	\N	f	\N	\N	1	\N
8	34  E  00080	nassau	1	34	E	  	80	8  LEXINGTON CIR	LEXINGTON	8 	NY	1091839	199946	2100	2019-12-15	494123	1958	1862	f	1	\N	4	\N	0.184299999999999992	20	2	1	\N	f	\N	\N	1	\N
9	34  E  00630	nassau	1	34	E	  	630	20  WARNER AVE	WARNER	20 	NY	1092026	198875	2100	2019-12-15	643944	1936	1855	f	1	\N	4	\N	0.137699999999999989	24	1	1	\N	f	\N	\N	1	\N
10	34  E  00660	nassau	1	34	E	  	660	28  WARNER AVE	WARNER	28 	NY	1092013	198934	2100	2019-12-15	592460	1951	1534	f	1	\N	4	\N	0.137699999999999989		2	0	\N	f	\N	\N	1	\N
11	34  E  00690	nassau	1	34	E	  	690	32  WARNER AVE	WARNER	32 	NY	1092000	198992	2100	2019-12-15	600830	1936	1415	f	1	\N	4	\N	0.137699999999999989		2	0	\N	f	\N	\N	1	\N
12	34  E  00720	nassau	1	34	E	  	720	  WARNER AVE	WARNER	 	NY	1091988	199050	3111	2019-12-15	310457	\N	\N	f	1	\N		\N	0.137699999999999989		\N	\N	\N	f	\N	\N	1	\N
13	34  E  00750	nassau	1	34	E	  	750	48  WARNER AVE	WARNER	48 	NY	1091974	199111	2100	2019-12-15	461617	1948	2473	f	1	1	4	\N	0.229599999999999999		2	1	\N	f	\N	\N	1	\N
14	34  E  00800	nassau	1	34	E	  	800	56  WARNER AVE	WARNER	56 	NY	1091953	199210	2100	2019-12-15	757999	1928	1834	f	1	\N	4	\N	0.137699999999999989	20	1	1	\N	f	\N	\N	1	\N
15	34  E  00830	nassau	1	34	E	  	830	62  WARNER AVE	WARNER	62 	NY	1091940	199269	2100	2019-12-15	701215	1955	1456	f	1	\N	4	\N	0.137699999999999989		1	0	\N	f	\N	\N	1	\N
16	07231  00180	nassau	3	7	231	  	180	7  EDGEWOOD LN	EDGEWOOD	7 	NY	1087464	233134	2100	2019-12-15	612440	1955	2024	f	1	\N	4	\N	0.506199999999999983	20	3	0	\N	f	\N	\N	2	\N
\.


--
-- Data for Name: property_validation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.property_validation (id, apn, county, errors) FROM stdin;
\.


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.role (id, name, description) FROM stdin;
1	admin	admin
2	user	user
3	guest	guest
\.


--
-- Data for Name: roles_users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles_users (user_id, role_id) FROM stdin;
1	1
1	3
\.


--
-- Data for Name: ruleset; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ruleset (id, county, township, proximity, price_from, price_to, date_from, date_to, same_class, same_style, same_street) FROM stdin;
\.


--
-- Data for Name: selection_rules; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.selection_rules (id, proximity_range) FROM stdin;
1	0.200
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, username, password, active, confirmed_at) FROM stdin;
1	jev@alandarev.com	jev	$6$rounds=656000$M0mfz8NyE1UFzYZ3$DOhOllH7E9ZVa8UEhjeTL8//0D99QcTe5QLTBIA8Pi0xQ/XU3LN/yuhhPTBLPeRond2peJ1kbuL1rba9s7H9q1	t	\N
\.


--
-- Name: assessment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.assessment_id_seq', 1, false);


--
-- Name: assessment_validation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.assessment_validation_id_seq', 1, false);


--
-- Name: inventory_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.inventory_rules_id_seq', 1, true);


--
-- Name: property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.property_id_seq', 1, false);


--
-- Name: property_validation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.property_validation_id_seq', 1, false);


--
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.role_id_seq', 3, true);


--
-- Name: ruleset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ruleset_id_seq', 1, false);


--
-- Name: selection_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.selection_rules_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: property _apn_county_uc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.property
    ADD CONSTRAINT _apn_county_uc UNIQUE (apn, county);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: assessment assessment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment
    ADD CONSTRAINT assessment_pkey PRIMARY KEY (id);


--
-- Name: assessment_validation assessment_validation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_validation
    ADD CONSTRAINT assessment_validation_pkey PRIMARY KEY (id);


--
-- Name: inventory_rules inventory_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_rules
    ADD CONSTRAINT inventory_rules_pkey PRIMARY KEY (id);


--
-- Name: property property_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.property
    ADD CONSTRAINT property_pkey PRIMARY KEY (id);


--
-- Name: property_validation property_validation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.property_validation
    ADD CONSTRAINT property_validation_pkey PRIMARY KEY (id);


--
-- Name: role role_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_name_key UNIQUE (name);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: ruleset ruleset_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ruleset
    ADD CONSTRAINT ruleset_pkey PRIMARY KEY (id);


--
-- Name: selection_rules selection_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.selection_rules
    ADD CONSTRAINT selection_rules_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_property_apn; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_property_apn ON public.property USING btree (apn);


--
-- Name: assessment assessment_apn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment
    ADD CONSTRAINT assessment_apn_fkey FOREIGN KEY (apn, county) REFERENCES public.property(apn, county);


--
-- Name: property_validation property_validation_apn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.property_validation
    ADD CONSTRAINT property_validation_apn_fkey FOREIGN KEY (apn, county) REFERENCES public.property(apn, county);


--
-- Name: roles_users roles_users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_users
    ADD CONSTRAINT roles_users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id);


--
-- Name: roles_users roles_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles_users
    ADD CONSTRAINT roles_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

