--
-- PostgreSQL database dump
--

\restrict 9IhE0dh8pTBdbFWH8ZqbTzQffmZHuOvWF7KUG8gdx64qcn6Rg1tGR4hXcFXYyFi

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

-- Started on 2025-12-19 01:50:37

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5055 (class 1262 OID 16388)
-- Name: cake_site; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE cake_site WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';


ALTER DATABASE cake_site OWNER TO postgres;

\unrestrict 9IhE0dh8pTBdbFWH8ZqbTzQffmZHuOvWF7KUG8gdx64qcn6Rg1tGR4hXcFXYyFi
\connect cake_site
\restrict 9IhE0dh8pTBdbFWH8ZqbTzQffmZHuOvWF7KUG8gdx64qcn6Rg1tGR4hXcFXYyFi

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 876 (class 1247 OID 17440)
-- Name: deliverytype; Type: TYPE; Schema: public; Owner: cake_user
--

CREATE TYPE public.deliverytype AS ENUM (
    'PICKUP',
    'DELIVERY'
);


ALTER TYPE public.deliverytype OWNER TO cake_user;

--
-- TOC entry 873 (class 1247 OID 17426)
-- Name: orderstatus; Type: TYPE; Schema: public; Owner: cake_user
--

CREATE TYPE public.orderstatus AS ENUM (
    'PENDING',
    'CONFIRMED',
    'IN_PROGRESS',
    'READY',
    'DELIVERED',
    'CANCELLED'
);


ALTER TYPE public.orderstatus OWNER TO cake_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 17401)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO cake_user;

--
-- TOC entry 223 (class 1259 OID 17468)
-- Name: cake_layers; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.cake_layers (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    price_per_unit double precision NOT NULL,
    is_available boolean
);


ALTER TABLE public.cake_layers OWNER TO cake_user;

--
-- TOC entry 222 (class 1259 OID 17467)
-- Name: cake_layers_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.cake_layers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cake_layers_id_seq OWNER TO cake_user;

--
-- TOC entry 5058 (class 0 OID 0)
-- Dependencies: 222
-- Name: cake_layers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.cake_layers_id_seq OWNED BY public.cake_layers.id;


--
-- TOC entry 221 (class 1259 OID 17458)
-- Name: cakes; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.cakes (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    price double precision NOT NULL,
    image_url character varying,
    is_available boolean,
    weight double precision,
    ingredients text
);


ALTER TABLE public.cakes OWNER TO cake_user;

--
-- TOC entry 220 (class 1259 OID 17457)
-- Name: cakes_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.cakes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cakes_id_seq OWNER TO cake_user;

--
-- TOC entry 5059 (class 0 OID 0)
-- Dependencies: 220
-- Name: cakes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.cakes_id_seq OWNED BY public.cakes.id;


--
-- TOC entry 241 (class 1259 OID 17600)
-- Name: chat_connections; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.chat_connections (
    id integer NOT NULL,
    user_id integer NOT NULL,
    room_id integer NOT NULL,
    connection_id character varying(255) NOT NULL,
    is_active boolean DEFAULT true,
    connected_at timestamp with time zone DEFAULT now(),
    disconnected_at timestamp with time zone
);


ALTER TABLE public.chat_connections OWNER TO cake_user;

--
-- TOC entry 240 (class 1259 OID 17599)
-- Name: chat_connections_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.chat_connections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chat_connections_id_seq OWNER TO cake_user;

--
-- TOC entry 5060 (class 0 OID 0)
-- Dependencies: 240
-- Name: chat_connections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.chat_connections_id_seq OWNED BY public.chat_connections.id;


--
-- TOC entry 239 (class 1259 OID 17579)
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.chat_messages (
    id integer NOT NULL,
    room_id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL,
    is_read boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.chat_messages OWNER TO cake_user;

--
-- TOC entry 238 (class 1259 OID 17578)
-- Name: chat_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.chat_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chat_messages_id_seq OWNER TO cake_user;

--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 238
-- Name: chat_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.chat_messages_id_seq OWNED BY public.chat_messages.id;


--
-- TOC entry 237 (class 1259 OID 17566)
-- Name: chat_rooms; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.chat_rooms (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.chat_rooms OWNER TO cake_user;

--
-- TOC entry 236 (class 1259 OID 17565)
-- Name: chat_rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.chat_rooms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chat_rooms_id_seq OWNER TO cake_user;

--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 236
-- Name: chat_rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.chat_rooms_id_seq OWNED BY public.chat_rooms.id;


--
-- TOC entry 225 (class 1259 OID 17478)
-- Name: creams; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.creams (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    price_per_unit double precision NOT NULL,
    is_available boolean
);


ALTER TABLE public.creams OWNER TO cake_user;

--
-- TOC entry 224 (class 1259 OID 17477)
-- Name: creams_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.creams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.creams_id_seq OWNER TO cake_user;

--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 224
-- Name: creams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.creams_id_seq OWNED BY public.creams.id;


--
-- TOC entry 231 (class 1259 OID 17508)
-- Name: custom_cakes; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.custom_cakes (
    id integer NOT NULL,
    user_id integer,
    name character varying,
    layers json,
    creams json,
    fillings json,
    decorations json,
    total_price double precision NOT NULL,
    weight double precision,
    description character varying
);


ALTER TABLE public.custom_cakes OWNER TO cake_user;

--
-- TOC entry 230 (class 1259 OID 17507)
-- Name: custom_cakes_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.custom_cakes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.custom_cakes_id_seq OWNER TO cake_user;

--
-- TOC entry 5064 (class 0 OID 0)
-- Dependencies: 230
-- Name: custom_cakes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.custom_cakes_id_seq OWNED BY public.custom_cakes.id;


--
-- TOC entry 229 (class 1259 OID 17498)
-- Name: decorations; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.decorations (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    price_per_unit double precision NOT NULL,
    is_available boolean
);


ALTER TABLE public.decorations OWNER TO cake_user;

--
-- TOC entry 228 (class 1259 OID 17497)
-- Name: decorations_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.decorations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.decorations_id_seq OWNER TO cake_user;

--
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 228
-- Name: decorations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.decorations_id_seq OWNED BY public.decorations.id;


--
-- TOC entry 227 (class 1259 OID 17488)
-- Name: fillings; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.fillings (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    price_per_unit double precision NOT NULL,
    is_available boolean
);


ALTER TABLE public.fillings OWNER TO cake_user;

--
-- TOC entry 226 (class 1259 OID 17487)
-- Name: fillings_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.fillings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fillings_id_seq OWNER TO cake_user;

--
-- TOC entry 5066 (class 0 OID 0)
-- Dependencies: 226
-- Name: fillings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.fillings_id_seq OWNED BY public.fillings.id;


--
-- TOC entry 233 (class 1259 OID 17523)
-- Name: orders; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    user_id integer,
    order_date timestamp with time zone DEFAULT now(),
    status public.orderstatus,
    total_amount double precision NOT NULL,
    delivery_type public.deliverytype NOT NULL,
    delivery_address character varying,
    delivery_date timestamp with time zone,
    customer_notes character varying,
    cake_id integer,
    custom_cake_id integer,
    quantity integer
);


ALTER TABLE public.orders OWNER TO cake_user;

--
-- TOC entry 232 (class 1259 OID 17522)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO cake_user;

--
-- TOC entry 5067 (class 0 OID 0)
-- Dependencies: 232
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- TOC entry 235 (class 1259 OID 17549)
-- Name: payments; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    order_id integer,
    amount double precision NOT NULL,
    payment_date timestamp with time zone DEFAULT now(),
    payment_method character varying,
    payment_status character varying,
    transaction_id character varying
);


ALTER TABLE public.payments OWNER TO cake_user;

--
-- TOC entry 234 (class 1259 OID 17548)
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO cake_user;

--
-- TOC entry 5068 (class 0 OID 0)
-- Dependencies: 234
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- TOC entry 219 (class 1259 OID 17446)
-- Name: users; Type: TABLE; Schema: public; Owner: cake_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    full_name character varying NOT NULL,
    phone character varying,
    address character varying,
    is_active boolean,
    is_admin boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO cake_user;

--
-- TOC entry 218 (class 1259 OID 17445)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: cake_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO cake_user;

--
-- TOC entry 5069 (class 0 OID 0)
-- Dependencies: 218
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cake_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4810 (class 2604 OID 17471)
-- Name: cake_layers id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.cake_layers ALTER COLUMN id SET DEFAULT nextval('public.cake_layers_id_seq'::regclass);


--
-- TOC entry 4809 (class 2604 OID 17461)
-- Name: cakes id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.cakes ALTER COLUMN id SET DEFAULT nextval('public.cakes_id_seq'::regclass);


--
-- TOC entry 4825 (class 2604 OID 17603)
-- Name: chat_connections id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_connections ALTER COLUMN id SET DEFAULT nextval('public.chat_connections_id_seq'::regclass);


--
-- TOC entry 4822 (class 2604 OID 17582)
-- Name: chat_messages id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_messages ALTER COLUMN id SET DEFAULT nextval('public.chat_messages_id_seq'::regclass);


--
-- TOC entry 4819 (class 2604 OID 17569)
-- Name: chat_rooms id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_rooms ALTER COLUMN id SET DEFAULT nextval('public.chat_rooms_id_seq'::regclass);


--
-- TOC entry 4811 (class 2604 OID 17481)
-- Name: creams id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.creams ALTER COLUMN id SET DEFAULT nextval('public.creams_id_seq'::regclass);


--
-- TOC entry 4814 (class 2604 OID 17511)
-- Name: custom_cakes id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.custom_cakes ALTER COLUMN id SET DEFAULT nextval('public.custom_cakes_id_seq'::regclass);


--
-- TOC entry 4813 (class 2604 OID 17501)
-- Name: decorations id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.decorations ALTER COLUMN id SET DEFAULT nextval('public.decorations_id_seq'::regclass);


--
-- TOC entry 4812 (class 2604 OID 17491)
-- Name: fillings id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.fillings ALTER COLUMN id SET DEFAULT nextval('public.fillings_id_seq'::regclass);


--
-- TOC entry 4815 (class 2604 OID 17526)
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- TOC entry 4817 (class 2604 OID 17552)
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- TOC entry 4807 (class 2604 OID 17449)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5025 (class 0 OID 17401)
-- Dependencies: 217
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.alembic_version (version_num) VALUES ('8211f200876b');


--
-- TOC entry 5031 (class 0 OID 17468)
-- Dependencies: 223
-- Data for Name: cake_layers; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.cake_layers (id, name, description, price_per_unit, is_available) VALUES (1, 'бисквитный', 'string', 200, false);
INSERT INTO public.cake_layers (id, name, description, price_per_unit, is_available) VALUES (2, 'Слоёное тесто', NULL, 500, false);


--
-- TOC entry 5029 (class 0 OID 17458)
-- Dependencies: 221
-- Data for Name: cakes; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.cakes (id, name, description, price, image_url, is_available, weight, ingredients) VALUES (1, 'Шоколадный торт', 'Очень вкусный', 1000, 'https://s.yimg.com/ny/api/res/1.2/Qar_FF9L9IuBMcOHwPbcCA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTUzOTtjZj13ZWJw/https://media.zenfs.com/en/tasting_table_543/e8f09b4436d8ae1c7b53b0db3d59baf3', true, 900, 'Шоколад!!!!!');
INSERT INTO public.cakes (id, name, description, price, image_url, is_available, weight, ingredients) VALUES (2, 'Красный бархат', 'Любимый торт моей девушки', 2000, 'https://cdnn21.img.ria.ru/images/07e9/02/05/1997582907_3:0:1454:816_1280x0_80_0_0_482773d78ffcdba4ed4d67269d0e34d7.jpg', true, 1000, NULL);
INSERT INTO public.cakes (id, name, description, price, image_url, is_available, weight, ingredients) VALUES (5, 'Новый', NULL, 10, NULL, true, 10, NULL);


--
-- TOC entry 5049 (class 0 OID 17600)
-- Dependencies: 241
-- Data for Name: chat_connections; Type: TABLE DATA; Schema: public; Owner: cake_user
--



--
-- TOC entry 5047 (class 0 OID 17579)
-- Dependencies: 239
-- Data for Name: chat_messages; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (1, 1, 1, 'Привет всем!', false, '2025-12-16 12:48:24.33933+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (2, 1, 1, 'Привет всем!', false, '2025-12-16 12:49:24.229243+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (3, 1, 2, 'yjdjt', false, '2025-12-16 12:51:03.104215+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (4, 1, 2, 'Привет', false, '2025-12-16 13:04:37.135995+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (5, 1, 1, 'И тебе привет', false, '2025-12-16 13:05:02.280932+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (6, 1, 2, 'Новое сообщение', false, '2025-12-16 13:20:20.797465+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (7, 1, 1, 'Привет', false, '2025-12-16 13:19:30.445704+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (8, 1, 2, 'Привет', false, '2025-12-16 13:34:37.517766+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (9, 1, 1, 'Новое сообщение', false, '2025-12-16 13:33:58.247732+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (10, 1, 2, 'Привет', false, '2025-12-16 13:34:39.728436+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (11, 1, 3, 'Есть вопрос', false, '2025-12-16 13:37:10.615436+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (12, 1, 2, ' Важное обновление завтра в 10:00', false, '2025-12-16 13:41:58.614041+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (13, 1, 1, 'Новое сообщение', false, '2025-12-16 13:41:51.472693+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (14, 1, 2, ' Важное обновление завтра в 10:00', false, '2025-12-16 13:42:00.248996+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (15, 1, 1, 'Новое сообщение', false, '2025-12-16 13:42:32.651974+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (16, 1, 2, '@Admin Важное обновление завтра в 10:00', false, '2025-12-16 13:44:49.726108+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (17, 1, 2, '@Admin Важное обновление завтра в 10:00', false, '2025-12-16 13:44:53.174152+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (18, 1, 1, '@Admin yjdjt', false, '2025-12-16 13:44:56.554639+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (19, 1, 1, '@user1 Ваш заказ готов', false, '2025-12-16 13:45:22.889332+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (20, 1, 3, 'Есть вопрос', false, '2025-12-16 14:01:34.254937+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (21, 1, 1, '@user1 Ваш заказ готов', false, '2025-12-16 14:01:10.18804+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (22, 1, 1, '@user1 Ваш заказ готов', false, '2025-12-16 14:01:43.923292+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (23, 1, 1, 'Ваш заказ готов', false, '2025-12-16 14:03:52.026839+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (24, 1, 3, 'Есть вопрос', false, '2025-12-16 14:03:13.023232+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (25, 1, 1, 'Привет', false, '2025-12-18 11:06:57.796745+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (26, 1, 3, 'Есть вопрос', false, '2025-12-18 11:07:46.933971+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (27, 1, 1, 'слушаю вас', false, '2025-12-18 11:07:05.038658+07');
INSERT INTO public.chat_messages (id, room_id, user_id, message, is_read, created_at) VALUES (28, 1, 1, ' технические изменения', false, '2025-12-18 11:08:15.858273+07');


--
-- TOC entry 5045 (class 0 OID 17566)
-- Dependencies: 237
-- Data for Name: chat_rooms; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.chat_rooms (id, name, description, is_active, created_at, updated_at) VALUES (1, 'Главный чат', 'Основная комната для общения', true, '2025-12-15 22:09:21.440771+07', NULL);
INSERT INTO public.chat_rooms (id, name, description, is_active, created_at, updated_at) VALUES (2, 'prob', 'string', true, '2025-12-15 22:57:59.062798+07', NULL);


--
-- TOC entry 5033 (class 0 OID 17478)
-- Dependencies: 225
-- Data for Name: creams; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.creams (id, name, description, price_per_unit, is_available) VALUES (1, 'шоколадный крем', 'string', 500, true);
INSERT INTO public.creams (id, name, description, price_per_unit, is_available) VALUES (2, 'Сметанный', NULL, 500, true);


--
-- TOC entry 5039 (class 0 OID 17508)
-- Dependencies: 231
-- Data for Name: custom_cakes; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.custom_cakes (id, user_id, name, layers, creams, fillings, decorations, total_price, weight, description) VALUES (1, 1, 'Мой кастомный торт', '[{"id": 1, "quantity": 1}]', '[{"id": 1, "quantity": 2}]', '[{"id": 1, "quantity": 1}]', '[{"id": 1, "quantity": 1}]', 1350, 240, 'Кастомный торт Мой кастомный торт');


--
-- TOC entry 5037 (class 0 OID 17498)
-- Dependencies: 229
-- Data for Name: decorations; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.decorations (id, name, description, price_per_unit, is_available) VALUES (1, 'надпись', 'string', 0, true);


--
-- TOC entry 5035 (class 0 OID 17488)
-- Dependencies: 227
-- Data for Name: fillings; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.fillings (id, name, description, price_per_unit, is_available) VALUES (1, 'Варение', 'string', 150, true);
INSERT INTO public.fillings (id, name, description, price_per_unit, is_available) VALUES (2, 'Брусничный джем', NULL, 350, true);


--
-- TOC entry 5041 (class 0 OID 17523)
-- Dependencies: 233
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.orders (id, user_id, order_date, status, total_amount, delivery_type, delivery_address, delivery_date, customer_notes, cake_id, custom_cake_id, quantity) VALUES (1, 1, '2025-12-14 12:25:16.723663+07', 'CONFIRMED', 1350, 'PICKUP', NULL, NULL, 'Кастомный торт: Мой кастомный торт', NULL, 1, 1);
INSERT INTO public.orders (id, user_id, order_date, status, total_amount, delivery_type, delivery_address, delivery_date, customer_notes, cake_id, custom_cake_id, quantity) VALUES (2, 1, '2025-12-14 16:55:14.532891+07', 'CONFIRMED', 1000, 'PICKUP', NULL, NULL, 'Заказ торта "Шоколадный торт"', 1, NULL, 1);
INSERT INTO public.orders (id, user_id, order_date, status, total_amount, delivery_type, delivery_address, delivery_date, customer_notes, cake_id, custom_cake_id, quantity) VALUES (3, 1, '2025-12-14 17:27:56.122654+07', 'PENDING', 2000, 'PICKUP', NULL, NULL, 'Заказ торта "Красный бархат"', 2, NULL, 1);
INSERT INTO public.orders (id, user_id, order_date, status, total_amount, delivery_type, delivery_address, delivery_date, customer_notes, cake_id, custom_cake_id, quantity) VALUES (4, 2, '2025-12-14 17:43:16.434551+07', 'CONFIRMED', 2000, 'PICKUP', NULL, NULL, 'Заказ торта "Красный бархат"', 2, NULL, 1);


--
-- TOC entry 5043 (class 0 OID 17549)
-- Dependencies: 235
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.payments (id, order_id, amount, payment_date, payment_method, payment_status, transaction_id) VALUES (1, 1, 1350, '2025-12-14 16:16:04.084918+07', 'card', 'completed', 'txn_1_card');
INSERT INTO public.payments (id, order_id, amount, payment_date, payment_method, payment_status, transaction_id) VALUES (2, 2, 1000, '2025-12-14 16:55:19.218399+07', 'card', 'completed', 'txn_2_card');
INSERT INTO public.payments (id, order_id, amount, payment_date, payment_method, payment_status, transaction_id) VALUES (3, 4, 2000, '2025-12-14 17:43:26.871569+07', 'card', 'completed', 'txn_4_card');


--
-- TOC entry 5027 (class 0 OID 17446)
-- Dependencies: 219
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: cake_user
--

INSERT INTO public.users (id, email, password, full_name, phone, address, is_active, is_admin, created_at, updated_at) VALUES (1, 'inaydukov@mail.ru', '$2b$12$trwy06nwqoXOSnVTPWKPFuGh1AFEc5comyAClDwmuzFGI2b9W6JI2', 'Admin', '89138484307', '', true, true, '2025-12-14 12:20:33.594923+07', NULL);
INSERT INTO public.users (id, email, password, full_name, phone, address, is_active, is_admin, created_at, updated_at) VALUES (2, 'user@example.com', '$2b$12$lC1wpXJZpMbvpHX71hTdZOD7bosxzlCNay.gMvgcFAC2Lf9wZ9oV2', 'user', '88888888888', 'ул. Примерная, д. 1, кв. 2', true, true, '2025-12-14 17:42:32.860428+07', '2025-12-15 02:40:58.689518+07');
INSERT INTO public.users (id, email, password, full_name, phone, address, is_active, is_admin, created_at, updated_at) VALUES (3, 'new@mail.ru', '$2b$12$2he5mkss0RHBhAQgGJZ/D.OZsos2bqTlQQEmvk/7tg8GhLsYdHx3a', 'user1', '+8567222069827', 'string', true, false, '2025-12-16 13:36:10.815552+07', NULL);


--
-- TOC entry 5070 (class 0 OID 0)
-- Dependencies: 222
-- Name: cake_layers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.cake_layers_id_seq', 2, true);


--
-- TOC entry 5071 (class 0 OID 0)
-- Dependencies: 220
-- Name: cakes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.cakes_id_seq', 5, true);


--
-- TOC entry 5072 (class 0 OID 0)
-- Dependencies: 240
-- Name: chat_connections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.chat_connections_id_seq', 1, false);


--
-- TOC entry 5073 (class 0 OID 0)
-- Dependencies: 238
-- Name: chat_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.chat_messages_id_seq', 28, true);


--
-- TOC entry 5074 (class 0 OID 0)
-- Dependencies: 236
-- Name: chat_rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.chat_rooms_id_seq', 2, true);


--
-- TOC entry 5075 (class 0 OID 0)
-- Dependencies: 224
-- Name: creams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.creams_id_seq', 2, true);


--
-- TOC entry 5076 (class 0 OID 0)
-- Dependencies: 230
-- Name: custom_cakes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.custom_cakes_id_seq', 1, true);


--
-- TOC entry 5077 (class 0 OID 0)
-- Dependencies: 228
-- Name: decorations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.decorations_id_seq', 1, true);


--
-- TOC entry 5078 (class 0 OID 0)
-- Dependencies: 226
-- Name: fillings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.fillings_id_seq', 2, true);


--
-- TOC entry 5079 (class 0 OID 0)
-- Dependencies: 232
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.orders_id_seq', 4, true);


--
-- TOC entry 5080 (class 0 OID 0)
-- Dependencies: 234
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.payments_id_seq', 3, true);


--
-- TOC entry 5081 (class 0 OID 0)
-- Dependencies: 218
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cake_user
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- TOC entry 4829 (class 2606 OID 17405)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 4838 (class 2606 OID 17475)
-- Name: cake_layers cake_layers_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.cake_layers
    ADD CONSTRAINT cake_layers_pkey PRIMARY KEY (id);


--
-- TOC entry 4835 (class 2606 OID 17465)
-- Name: cakes cakes_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.cakes
    ADD CONSTRAINT cakes_pkey PRIMARY KEY (id);


--
-- TOC entry 4868 (class 2606 OID 17607)
-- Name: chat_connections chat_connections_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_connections
    ADD CONSTRAINT chat_connections_pkey PRIMARY KEY (id);


--
-- TOC entry 4863 (class 2606 OID 17588)
-- Name: chat_messages chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_pkey PRIMARY KEY (id);


--
-- TOC entry 4859 (class 2606 OID 17577)
-- Name: chat_rooms chat_rooms_name_key; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_rooms
    ADD CONSTRAINT chat_rooms_name_key UNIQUE (name);


--
-- TOC entry 4861 (class 2606 OID 17575)
-- Name: chat_rooms chat_rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_rooms
    ADD CONSTRAINT chat_rooms_pkey PRIMARY KEY (id);


--
-- TOC entry 4841 (class 2606 OID 17485)
-- Name: creams creams_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.creams
    ADD CONSTRAINT creams_pkey PRIMARY KEY (id);


--
-- TOC entry 4850 (class 2606 OID 17515)
-- Name: custom_cakes custom_cakes_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.custom_cakes
    ADD CONSTRAINT custom_cakes_pkey PRIMARY KEY (id);


--
-- TOC entry 4847 (class 2606 OID 17505)
-- Name: decorations decorations_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.decorations
    ADD CONSTRAINT decorations_pkey PRIMARY KEY (id);


--
-- TOC entry 4844 (class 2606 OID 17495)
-- Name: fillings fillings_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.fillings
    ADD CONSTRAINT fillings_pkey PRIMARY KEY (id);


--
-- TOC entry 4854 (class 2606 OID 17531)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 4857 (class 2606 OID 17557)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- TOC entry 4833 (class 2606 OID 17454)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4869 (class 1259 OID 17622)
-- Name: idx_chat_connections_connection_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX idx_chat_connections_connection_id ON public.chat_connections USING btree (connection_id);


--
-- TOC entry 4870 (class 1259 OID 17621)
-- Name: idx_chat_connections_user_room; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX idx_chat_connections_user_room ON public.chat_connections USING btree (user_id, room_id);


--
-- TOC entry 4864 (class 1259 OID 17620)
-- Name: idx_chat_messages_created_at; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX idx_chat_messages_created_at ON public.chat_messages USING btree (created_at);


--
-- TOC entry 4865 (class 1259 OID 17618)
-- Name: idx_chat_messages_room_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX idx_chat_messages_room_id ON public.chat_messages USING btree (room_id);


--
-- TOC entry 4866 (class 1259 OID 17619)
-- Name: idx_chat_messages_user_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX idx_chat_messages_user_id ON public.chat_messages USING btree (user_id);


--
-- TOC entry 4839 (class 1259 OID 17476)
-- Name: ix_cake_layers_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_cake_layers_id ON public.cake_layers USING btree (id);


--
-- TOC entry 4836 (class 1259 OID 17466)
-- Name: ix_cakes_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_cakes_id ON public.cakes USING btree (id);


--
-- TOC entry 4842 (class 1259 OID 17486)
-- Name: ix_creams_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_creams_id ON public.creams USING btree (id);


--
-- TOC entry 4851 (class 1259 OID 17521)
-- Name: ix_custom_cakes_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_custom_cakes_id ON public.custom_cakes USING btree (id);


--
-- TOC entry 4848 (class 1259 OID 17506)
-- Name: ix_decorations_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_decorations_id ON public.decorations USING btree (id);


--
-- TOC entry 4845 (class 1259 OID 17496)
-- Name: ix_fillings_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_fillings_id ON public.fillings USING btree (id);


--
-- TOC entry 4852 (class 1259 OID 17547)
-- Name: ix_orders_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_orders_id ON public.orders USING btree (id);


--
-- TOC entry 4855 (class 1259 OID 17563)
-- Name: ix_payments_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_payments_id ON public.payments USING btree (id);


--
-- TOC entry 4830 (class 1259 OID 17456)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 4831 (class 1259 OID 17455)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: cake_user
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- TOC entry 4878 (class 2606 OID 17608)
-- Name: chat_connections chat_connections_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_connections
    ADD CONSTRAINT chat_connections_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.chat_rooms(id) ON DELETE CASCADE;


--
-- TOC entry 4879 (class 2606 OID 17613)
-- Name: chat_connections chat_connections_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_connections
    ADD CONSTRAINT chat_connections_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4876 (class 2606 OID 17589)
-- Name: chat_messages chat_messages_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.chat_rooms(id) ON DELETE CASCADE;


--
-- TOC entry 4877 (class 2606 OID 17594)
-- Name: chat_messages chat_messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4871 (class 2606 OID 17516)
-- Name: custom_cakes custom_cakes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.custom_cakes
    ADD CONSTRAINT custom_cakes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4872 (class 2606 OID 17537)
-- Name: orders orders_cake_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_cake_id_fkey FOREIGN KEY (cake_id) REFERENCES public.cakes(id);


--
-- TOC entry 4873 (class 2606 OID 17542)
-- Name: orders orders_custom_cake_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_custom_cake_id_fkey FOREIGN KEY (custom_cake_id) REFERENCES public.custom_cakes(id);


--
-- TOC entry 4874 (class 2606 OID 17532)
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4875 (class 2606 OID 17558)
-- Name: payments payments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cake_user
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- TOC entry 5056 (class 0 OID 0)
-- Dependencies: 5055
-- Name: DATABASE cake_site; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON DATABASE cake_site TO cake_user;


--
-- TOC entry 5057 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO cake_user;


-- Completed on 2025-12-19 01:50:37

--
-- PostgreSQL database dump complete
--

\unrestrict 9IhE0dh8pTBdbFWH8ZqbTzQffmZHuOvWF7KUG8gdx64qcn6Rg1tGR4hXcFXYyFi

