import React, { useState, useEffect } from 'react';
import { TrendingUp, Folder, Zap, DollarSign, Star, Activity } from 'lucide-react';
import { getProjects } from '../services/api';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [stats, setStats] = useState({
    total_projects: 0,
    status_distribution: {},
    phase_distribution: {},
    avg_quality_score: 0,
    total_cost: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getProjects();
        const projectsData = response.data;
        setProjects(projectsData);
        
        // İstatistikleri hesapla
        const newStats = calculateStats(projectsData);
        setStats(newStats);
      } catch (error) {
        console.error('Veri yüklenirken hata:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const calculateStats = (projectsData) => {
    const total = projectsData.length;
    const statusDist = {};
    const phaseDist = {};
    let totalQuality = 0;
    let qualityCount = 0;
    let totalCost = 0;

    projectsData.forEach(project => {
      // Status dağılımı
      statusDist[project.status] = (statusDist[project.status] || 0) + 1;
      
      // Phase dağılımı  
      phaseDist[project.phase] = (phaseDist[project.phase] || 0) + 1;
      
      // Kalite skoru
      if (project.quality_score > 0) {
        totalQuality += project.quality_score;
        qualityCount++;
      }
      
      // Maliyet
      totalCost += project.cost || 0;
    });

    return {
      total_projects: total,
      status_distribution: statusDist,
      phase_distribution: phaseDist,
      avg_quality_score: qualityCount > 0 ? totalQuality / qualityCount : 0,
      total_cost: totalCost
    };
  };

  const getPhaseColor = (phase) => {
    const colors = {
      'planning': '#ff9500',
      'development': '#3b82f6', 
      'testing': '#f59e0b',
      'deployment': '#10b981'
    };
    return colors[phase] || '#6b7280';
  };

  const getStatusColor = (status) => {
    const colors = {
      'active': '#00d97e',
      'completed': '#3b82f6',
      'archived': '#6b7280'
    };
    return colors[status] || '#6b7280';
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '60vh' 
      }}>
        <div className="spinner"></div>
      </div>
    );
  }

  const recentProjects = projects.slice(0, 5);

  return (
    <div className="fade-in" style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ 
          fontSize: '32px', 
          fontWeight: 'bold', 
          color: 'var(--text)',
          marginBottom: '8px',
          fontFamily: 'Syne'
        }}>
          Dashboard
        </h1>
        <p style={{ color: 'var(--muted)', fontSize: '16px' }}>
          Proje yönetimi genel bakış
        </p>
      </div>

      {/* Stats Cards */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
        gap: '20px',
        marginBottom: '32px'
      }}>
        <div style={{
          background: 'linear-gradient(145deg, #1a1a26 0%, #22222f 100%)',
          borderRadius: '16px',
          padding: '24px',
          border: '1px solid #2a2a3a'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
            <div style={{
              width: '48px', height: '48px',
              background: 'linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%)',
              borderRadius: '12px',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Folder size={24} color="white" />
            </div>
            <div>
              <p style={{ color: 'var(--muted)', fontSize: '14px' }}>Toplam Proje</p>
              <p style={{ color: 'var(--text)', fontSize: '24px', fontWeight: 'bold' }}>
                {stats.total_projects}
              </p>
            </div>
          </div>
        </div>

        <div style={{
          background: 'linear-gradient(145deg, #1a1a26 0%, #22222f 100%)',
          borderRadius: '16px',
          padding: '24px',
          border: '1px solid #2a2a3a'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
            <div style={{
              width: '48px', height: '48px',
              background: 'linear-gradient(135deg, var(--green) 0%, #00f5a0 100%)',
              borderRadius: '12px',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Star size={24} color="white" />
            </div>
            <div>
              <p style={{ color: 'var(--muted)', fontSize: '14px' }}>Ortalama Kalite</p>
              <p style={{ color: 'var(--text)', fontSize: '24px', fontWeight: 'bold' }}>
                {stats.avg_quality_score.toFixed(1)}/100
              </p>
            </div>
          </div>
        </div>

        <div style={{
          background: 'linear-gradient(145deg, #1a1a26 0%, #22222f 100%)',
          borderRadius: '16px',
          padding: '24px',
          border: '1px solid #2a2a3a'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
            <div style={{
              width: '48px', height: '48px',
              background: 'linear-gradient(135deg, var(--orange) 0%, #ffb340 100%)',
              borderRadius: '12px',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <DollarSign size={24} color="white" />
            </div>
            <div>
              <p style={{ color: 'var(--muted)', fontSize: '14px' }}>Toplam Maliyet</p>
              <p style={{ color: 'var(--text)', fontSize: '24px', fontWeight: 'bold' }}>
                ${stats.total_cost.toFixed(4)}
              </p>
            </div>
          </div>
        </div>

        <div style={{
          background: 'linear-gradient(145deg, #1a1a26 0%, #22222f 100%)',
          borderRadius: '16px',
          padding: '24px',
          border: '1px solid #2a2a3a'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
            <div style={{
              width: '48px', height: '48px',
              background: 'linear-gradient(135deg, var(--blue) 0%, #60a5fa 100%)',
              borderRadius: '12px',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Activity size={24} color="white" />
            </div>
            <div>
              <p style={{ color: 'var(--muted)', fontSize: '14px' }}>Aktif Projeler</p>
              <p style={{ color: 'var(--text)', fontSize: '24px', fontWeight: 'bold' }}>
                {stats.status_distribution.active || 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Projects & Distributions */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        {/* Recent Projects */}
        <div style={{
          background: 'var(--surface)',
          borderRadius: '16px',
          padding: '24px',
          border: '1px solid var(--border)'
        }}>
          <h3 style={{ 
            fontSize: '20px', 
            fontWeight: 'bold', 
            marginBottom: '20px',
            color: 'var(--text)'
          }}>
            Son Projeler
          </h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {recentProjects.map(project => (
              <div key={project.id} style={{
                background: 'var(--surface2)',
                borderRadius: '12px',
                padding: '16px',
                border: '1px solid var(--border2)',
                transition: 'all 0.2s ease'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                  <h4 style={{ color: 'var(--text)', fontSize: '16px', fontWeight: '500' }}>
                    Proje #{project.id}
                  </h4>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <div style={{
                      background: getPhaseColor(project.phase),
                      color: 'white',
                      padding: '4px 8px',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '500'
                    }}>
                      {project.phase}
                    </div>
                    <div style={{
                      background: getStatusColor(project.status),
                      color: 'white',
                      padding: '4px 8px',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '500'
                    }}>
                      {project.status}
                    </div>
                  </div>
                </div>
                
                <p style={{ 
                  color: 'var(--muted)', 
                  fontSize: '14px',
                  marginBottom: '12px',
                  lineHeight: '1.4'
                }}>
                  {project.brief.substring(0, 100)}...
                </p>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                  <span style={{ color: 'var(--muted)' }}>
                    Kalite: {project.quality_score.toFixed(1)}/100
                  </span>
                  <span style={{ color: 'var(--muted)' }}>
                    Maliyet: ${project.cost.toFixed(4)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Distribution Charts */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Phase Distribution */}
          <div style={{
            background: 'var(--surface)',
            borderRadius: '16px',
            padding: '20px',
            border: '1px solid var(--border)'
          }}>
            <h4 style={{ 
              fontSize: '16px', 
              fontWeight: 'bold', 
              marginBottom: '16px',
              color: 'var(--text)'
            }}>
              Proje Aşamaları
            </h4>
            
            {Object.entries(stats.phase_distribution).map(([phase, count]) => (
              <div key={phase} style={{ marginBottom: '12px' }}>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  marginBottom: '4px' 
                }}>
                  <span style={{ color: 'var(--text)', fontSize: '14px' }}>{phase}</span>
                  <span style={{ color: 'var(--muted)', fontSize: '14px' }}>{count}</span>
                </div>
                <div style={{
                  background: 'var(--surface2)',
                  borderRadius: '4px',
                  height: '6px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    background: getPhaseColor(phase),
                    height: '100%',
                    width: `${(count / stats.total_projects) * 100}%`,
                    borderRadius: '4px'
                  }} />
                </div>
              </div>
            ))}
          </div>

          {/* Status Distribution */}
          <div style={{
            background: 'var(--surface)',
            borderRadius: '16px',
            padding: '20px',
            border: '1px solid var(--border)'
          }}>
            <h4 style={{ 
              fontSize: '16px', 
              fontWeight: 'bold', 
              marginBottom: '16px',
              color: 'var(--text)'
            }}>
              Proje Durumları
            </h4>
            
            {Object.entries(stats.status_distribution).map(([status, count]) => (
              <div key={status} style={{ marginBottom: '12px' }}>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  marginBottom: '4px' 
                }}>
                  <span style={{ color: 'var(--text)', fontSize: '14px' }}>{status}</span>
                  <span style={{ color: 'var(--muted)', fontSize: '14px' }}>{count}</span>
                </div>
                <div style={{
                  background: 'var(--surface2)',
                  borderRadius: '4px',
                  height: '6px',