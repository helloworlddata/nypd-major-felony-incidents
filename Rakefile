require 'pathname'
DATA_DIR = Pathname 'data'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR.join('corral')
SCRIPTS_DIR = WRANGLE_DIR.join('scripts')
DIRS = {
    :fetched => CORRAL_DIR.join('fetched'),
    :published => DATA_DIR,
}

START_YEAR = 2006
END_YEAR = 2016

F_FILES = Hash[(START_YEAR..END_YEAR).map{ |year| [year.to_s, DIRS[:fetched] / "#{year}.csv"]}]
F_FILES['2005-and-previous'] = DIRS[:fetched]/ '2005-and-previous.csv'



desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        unless p.exist?
            p.mkpath()
            puts "Created directory: #{p}"
        end
    end
end


namespace :publish do
    desc 'got to fetch them all'
    task :fetch => :setup do
        F_FILES.each_value{|fname| Rake::Task[fname].execute() }
    end
end



namespace :filings do
    F_FILES.each_pair do |year, fname|
        if year.to_s =~ /^20\d{2}$/
            desc "Fetch year #{year}"
            file fname => :setup do
                sh "python #{SCRIPTS_DIR.join('fetch_data.py')} #{year} > #{fname}"
            end
        end
    end

    # special case of 2005-and-previous
    year = 2005
    desc "Fetch 2005 and previous"
    fname = F_FILES['2005-and-previous']
    file fname => :setup do
        sh "python #{SCRIPTS_DIR.join('fetch_data.py')} #{year} --gte 1900 > #{fname}"
    end


end
