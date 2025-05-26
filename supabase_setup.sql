-- Create user_languages table
CREATE TABLE IF NOT EXISTS user_languages (
    user_id BIGINT PRIMARY KEY,
    language TEXT NOT NULL DEFAULT 'fr',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create user_favorites table
CREATE TABLE IF NOT EXISTS user_favorites (
    user_id BIGINT NOT NULL,
    stop_name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    PRIMARY KEY (user_id, stop_name)
);

-- Create user_reminders table
CREATE TABLE IF NOT EXISTS user_reminders (
    user_id BIGINT NOT NULL,
    line TEXT NOT NULL,
    stop TEXT NOT NULL,
    time TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    PRIMARY KEY (user_id, line, stop, time)
);

-- Create user_preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id BIGINT NOT NULL,
    setting TEXT NOT NULL,
    value TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    PRIMARY KEY (user_id, setting)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_languages_user_id ON user_languages(user_id);
CREATE INDEX IF NOT EXISTS idx_user_favorites_user_id ON user_favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_user_reminders_user_id ON user_reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);

-- Add RLS (Row Level Security) policies
ALTER TABLE user_languages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Create policies for each table
CREATE POLICY "Users can read their own language" ON user_languages
    FOR SELECT USING (user_id::text = auth.uid()::text);

CREATE POLICY "Users can update their own language" ON user_languages
    FOR UPDATE USING (user_id::text = auth.uid()::text);

CREATE POLICY "Users can insert their own language" ON user_languages
    FOR INSERT WITH CHECK (user_id::text = auth.uid()::text);

-- Similar policies for other tables
CREATE POLICY "Users can read their own favorites" ON user_favorites
    FOR SELECT USING (user_id::text = auth.uid()::text);

CREATE POLICY "Users can manage their own favorites" ON user_favorites
    FOR ALL USING (user_id::text = auth.uid()::text);

CREATE POLICY "Users can read their own reminders" ON user_reminders
    FOR SELECT USING (user_id::text = auth.uid()::text);

CREATE POLICY "Users can manage their own reminders" ON user_reminders
    FOR ALL USING (user_id::text = auth.uid()::text);

CREATE POLICY "Users can read their own preferences" ON user_preferences
    FOR SELECT USING (user_id::text = auth.uid()::text);

CREATE POLICY "Users can manage their own preferences" ON user_preferences
    FOR ALL USING (user_id::text = auth.uid()::text); 