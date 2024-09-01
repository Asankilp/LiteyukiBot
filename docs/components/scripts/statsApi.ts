
// URL
export const OWNER = "LiteyukiStudio"
export const REPO = "LiteyukiBot"
const githubAPIUrl = "https://api.github.com"
const onlineFetchUrl = "https://api.liteyuki.icu/online";
const totalFetchUrl = "https://api.liteyuki.icu/count";

export const RepoUrl = `https://github.com/${OWNER}/${REPO}`
export const StarMapUrl = "https://starmap.liteyuki.icu"

type GithubStats = {
    stars: number;
    forks: number;
    watchers: number;
    issues?: number;
    prs?: number;
    size?: number;
}

// 异步接口
interface StatsApi {
    getTotal: () => Promise<number>;
    getOnline: () => Promise<number>;
    getGithubStats: () => Promise<GithubStats>;
    getPluginNum: () => Promise<number>;
    getResourceNum: () => Promise<number>;
}


export type { GithubStats };

// 实现接口
export const statsApi: StatsApi = {
    getTotal: async () => {
        try {
            const res = await fetch(totalFetchUrl);
            const data = await res.json();
            return data.register;
        } catch (e) {
            return -1;
        }
    },
    getOnline: async () => {
        try {
            const res = await fetch(onlineFetchUrl);
            const data = await res.json();
            return data.online;
        } catch (e) {
            return -1;
        }
    },
    getGithubStats: async () => {
        try {
            const res = await fetch(`${githubAPIUrl}/repos/${OWNER}/${REPO}`);
            const data = await res.json();
            return {
                stars: data.stargazers_count,
                forks: data.forks_count,
                watchers: data.watchers_count,
                issues: data.open_issues_count,
                prs: data.open_issues_count,
                size: data.size,
            };
        } catch (e) {
            return {
                stars: -1,
                forks: -1,
                watchers: -1,
                issues: -1,
                prs: -1,
                size: -1,
            };
        }
    },
    getPluginNum: async () => {
        try {
            const res = await fetch('/plugins.json');
            const data = await res.json();
            return data.length;
        } catch (e) {
            return -1;
        }
    },
    getResourceNum: async () => {
        try {
            const res = await fetch('/resources.json');
            const data = await res.json();
            return data.length;
        } catch (e) {
            return -1;
        }
    }
};