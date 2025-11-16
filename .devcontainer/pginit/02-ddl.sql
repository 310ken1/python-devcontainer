-- Project Name : python_devcontainer
-- Date/Time    : 2025/11/16 22:14:59
-- Author       : 
-- RDBMS Type   : PostgreSQL
-- Application  : A5:SQL Mk-2

/*
  << 注意！！ >>
  BackupToTempTable, RestoreFromTempTable疑似命令が付加されています。
  これにより、drop table, create table 後もデータが残ります。
  この機能は一時的に $$TableName のような一時テーブルを作成します。
  この機能は A5:SQL Mk-2でのみ有効であることに注意してください。
*/

-- ロール権限
-- * BackupToTempTable
DROP TABLE if exists role_permissions CASCADE;

-- * RestoreFromTempTable
CREATE TABLE role_permissions (
  role_id bigint NOT NULL
  , permission_id bigint NOT NULL
  , CONSTRAINT role_permissions_PKC PRIMARY KEY (role_id,permission_id)
) ;

-- 認証情報
-- * BackupToTempTable
DROP TABLE if exists user_credentials CASCADE;

-- * RestoreFromTempTable
CREATE TABLE user_credentials (
  user_id bigint NOT NULL
  , password_hash character varying(255) NOT NULL
  , last_login_at timestamp(6) without time zone
  , failed_attempts integer DEFAULT 0 NOT NULL
  , locked_until timestamp(6) without time zone
  , updated_at timestamp(6) without time zone DEFAULT now() NOT NULL
  , CONSTRAINT user_credentials_PKC PRIMARY KEY (user_id)
) ;

-- ユーザロール
-- * BackupToTempTable
DROP TABLE if exists user_roles CASCADE;

-- * RestoreFromTempTable
CREATE TABLE user_roles (
  user_id bigint NOT NULL
  , role_id bigint NOT NULL
  , CONSTRAINT user_roles_PKC PRIMARY KEY (user_id,role_id)
) ;

-- ユーザ情報
-- * BackupToTempTable
DROP TABLE if exists users CASCADE;

-- * RestoreFromTempTable
CREATE TABLE users (
  user_id bigserial NOT NULL
  , email character varying(255) NOT NULL
  , username character varying(100)
  , display_name character varying(255)
  , is_active boolean DEFAULT true NOT NULL
  , created_at timestamp(6) without time zone DEFAULT now() NOT NULL
  , updated_at timestamp(6) without time zone DEFAULT now() NOT NULL
  , CONSTRAINT users_PKC PRIMARY KEY (user_id)
) ;

-- 権限
-- * BackupToTempTable
DROP TABLE if exists permissions CASCADE;

-- * RestoreFromTempTable
CREATE TABLE permissions (
  permission_id bigserial NOT NULL
  , name character varying(100) NOT NULL
  , description text
  , CONSTRAINT permissions_PKC PRIMARY KEY (permission_id)
) ;

-- ロール
-- * BackupToTempTable
DROP TABLE if exists roles CASCADE;

-- * RestoreFromTempTable
CREATE TABLE roles (
  role_id bigserial NOT NULL
  , name character varying(100) NOT NULL
  , description text
  , created_at timestamp(6) without time zone DEFAULT now() NOT NULL
  , CONSTRAINT roles_PKC PRIMARY KEY (role_id)
) ;

ALTER TABLE roles ADD CONSTRAINT roles_name_key
  UNIQUE (name) ;

COMMENT ON TABLE role_permissions IS 'ロール権限';
COMMENT ON COLUMN role_permissions.role_id IS 'role_id';
COMMENT ON COLUMN role_permissions.permission_id IS 'permission_id';

COMMENT ON TABLE user_credentials IS '認証情報:パスワードハッシュやログイン状態など、機密情報を分離して格納';
COMMENT ON COLUMN user_credentials.user_id IS 'ユーザID';
COMMENT ON COLUMN user_credentials.password_hash IS 'パスワードハッシュ';
COMMENT ON COLUMN user_credentials.last_login_at IS '最終ログイン日時';
COMMENT ON COLUMN user_credentials.failed_attempts IS '連続ログイン失敗回数';
COMMENT ON COLUMN user_credentials.locked_until IS 'ロック解除予定日時';
COMMENT ON COLUMN user_credentials.updated_at IS '更新日時';

COMMENT ON TABLE user_roles IS 'ユーザロール:ユーザに割り当てられているロール';
COMMENT ON COLUMN user_roles.user_id IS 'ユーザID';
COMMENT ON COLUMN user_roles.role_id IS 'ロールID';

COMMENT ON TABLE users IS 'ユーザ情報:認証情報とは分離し、プロフィールや状態のみを保持';
COMMENT ON COLUMN users.user_id IS 'ユーザID';
COMMENT ON COLUMN users.email IS 'メールアドレス';
COMMENT ON COLUMN users.username IS 'ユーザ名';
COMMENT ON COLUMN users.display_name IS '表示名';
COMMENT ON COLUMN users.is_active IS '有効／無効';
COMMENT ON COLUMN users.created_at IS '作成日時';
COMMENT ON COLUMN users.updated_at IS '更新日時';

COMMENT ON TABLE permissions IS '権限';
COMMENT ON COLUMN permissions.permission_id IS '権限ID';
COMMENT ON COLUMN permissions.name IS '権限名';
COMMENT ON COLUMN permissions.description IS '説明';

COMMENT ON TABLE roles IS 'ロール';
COMMENT ON COLUMN roles.role_id IS 'ロールID';
COMMENT ON COLUMN roles.name IS 'ロール名';
COMMENT ON COLUMN roles.description IS '説明';
COMMENT ON COLUMN roles.created_at IS '作成日時';

