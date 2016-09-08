require 'pathname'
DATA_DIR = Pathname 'catalog'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR.join('corral')
SCRIPTS = WRANGLE_DIR.join('scripts')
DIRS = {
    'fetched' => CORRAL_DIR.join('fetched'),
    'cleaned' => CORRAL_DIR.join('cleaned'),
    'published' => DATA_DIR,
    'samples' => DATA_DIR / 'samples'
}

START_YEAR = 2006
END_YEAR = 2015 # Only complete years are disclosed

F_FILES = {}
F_FILES['2005-and-previous'] = DIRS['fetched'] / '2005-and-previous.csv'
(START_YEAR..END_YEAR).each{ |year| F_FILES[year.to_s] =  DIRS['fetched'] / "#{year}.csv" }
C_FILES = {
    'all' => DIRS['cleaned'] / 'all.csv'
}
P_FILES = {
    'through-2009' => DIRS['published'] / 'nypd-major-felony-incidents-through-2009.csv',
    '2010-through-2015' => DIRS['published'] / 'nypd-major-felony-incidents-2010-through-2015.csv',
    '2010-excerpt' => DIRS['samples'] / '2010-excerpt.csv'
}


desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        unless p.exist?
            p.mkpath()
            puts "Created directory: #{p}"
        end
    end
end


desc 'Fetch all data'
task :fetch => :setup do
    F_FILES.each_value{|fname| Rake::Task[fname].execute() }
end

desc "Clean all data, compile into one file"
task :compile  do
    Rake::Task[C_FILES['all']].execute()
end

task :publish do
    P_FILES.each_value do |fname|
        Rake::Task[fname].execute()
    end
end



namespace :files do

    namespace :published do
        desc 'Publish data 2009 and previous'
        file P_FILES['through-2009'] => C_FILES['all'] do
            # pure ruby woooo
            open(P_FILES['through-2009'], 'w') do |wf|
                File.foreach(C_FILES['all']).with_index do |line, lineno|
                    wf.puts line if line < '2010' or lineno == 0
                end
            end
        end

        desc 'Publish data 2010 through 2015'
        file P_FILES['2010-through-2015'] => C_FILES['all'] do
            # pure ruby woooo
            open(P_FILES['2010-through-2015'], 'w') do |wf|
                File.foreach(C_FILES['all']).with_index do |line, lineno|
                    wf.puts line if (line > '2010' && line <= '2016') or lineno == 0
                end
            end
        end

        desc 'sample from year 2010'
        file P_FILES['2010-excerpt'] => C_FILES['all'] do
            srcfile = C_FILES['all']
            destfile = P_FILES['2010-excerpt']
            sh %Q{
                head -n 1 #{srcfile} > #{destfile};
                ack '^2010-03' #{srcfile} >> #{destfile}
            }

        end

    end

    desc "Create cleaned and sorted file from the fetched data"
    file C_FILES['all'] => F_FILES.values() do
        sh ["cat", F_FILES.values(), '|',
            'python', SCRIPTS / 'clean.py', '-',
            '|', 'csvsort -c 1 --no-inference', '>',

            C_FILES['all']
            ].join(' ')
    end


    F_FILES.each_pair do |year, fname|
        if year.to_s =~ /^20\d{2}$/
            desc "Fetch year #{year}"
            file fname => :setup do
                sh "python #{SCRIPTS.join('fetch_data.py')} #{year} > #{fname}"
            end
        end
    end

    # special case of 2005-and-previous
    year = 2005
    desc "Fetch 2005 and previous"
    fname = F_FILES['2005-and-previous']
    file fname => :setup do
        sh "python #{SCRIPTS.join('fetch_data.py')} #{year} --gte 1900 > #{fname}"
    end
end
